import requests
import numpy as np
import re
from difflib import SequenceMatcher
from pypdf import PdfReader
import faiss  # type: ignore

# =========================
# OLLAMA CONFIG
# =========================

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"


# =========================
# OLLAMA HELPERS
# =========================

def ollama_chat(messages, model="llama3.1:8b", temperature=0.0):
    response = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": model,
            "messages": messages,
            "options": {"temperature": temperature},
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def ollama_embed(texts, model="nomic-embed-text"):
    if isinstance(texts, str):
        texts = [texts]

    vectors = []
    for t in texts:
        r = requests.post(
            OLLAMA_EMBED_URL,
            json={"model": model, "prompt": t},
            timeout=60,
        )
        r.raise_for_status()
        vectors.append(np.array(r.json()["embedding"], dtype=np.float32))

    return np.vstack(vectors)


def _l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return x / norms


# =========================
# PDF + CHUNKING
# =========================

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += max(1, chunk_size - overlap)
    return chunks


# =========================
# RAG ENGINE
# =========================

class RAG:
    def __init__(self, chunks):
        self.chunks = chunks

        if not chunks:
            self.embeddings = np.zeros((0, 1), dtype=np.float32)
            self.index = None
            return

        self.embeddings = _l2_normalize(ollama_embed(chunks))
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def retrieve(self, question, k=2, min_sim=0.55):
        if self.index is None:
            return []

        q_emb = _l2_normalize(ollama_embed(question))
        sims, idx = self.index.search(q_emb.astype(np.float32), k)
        return [
            self.chunks[i]
            for i, s in zip(idx[0], sims[0])
            if float(s) >= min_sim
        ]


# =========================
# ANSWER GENERATION
# =========================

def rag_answer(question, context_chunks):
    context = "\n\n".join(context_chunks).strip()

    if context:
        sys = (
            "Odpowiadaj WYŁĄCZNIE na podstawie kontekstu. "
            "Jeśli w kontekście nie ma odpowiedzi, powiedz to wprost."
        )
        user = f"KONTEKST:\n{context}\n\nPYTANIE:\n{question}"
    else:
        sys = "Odpowiedz krótko na podstawie ogólnej wiedzy."
        user = question

    return ollama_chat(
        [{"role": "system", "content": sys},
         {"role": "user", "content": user}]
    )


# =========================
# UTILS
# =========================

def cosine_similarity(a, b):
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0


def split_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]\s+", text) if s.strip()]


# =========================
# HALLUCINATION DETECTORS
# =========================

def llm_detector(answer, context):
    if not context.strip():
        return 0.5

    scores = []
    for s in split_sentences(answer):
        try:
            score = float(ollama_chat([
                {"role": "system", "content": "Oceń 0-1 czy zdanie wynika WYŁĄCZNIE z kontekstu. Zwróć tylko liczbę."},
                {"role": "user", "content": f"KONTEKST:\n{context}\n\nZDANIE:\n{s}"}
            ]))
        except:
            score = 0.0
        scores.append(score)

    return 1.0 - float(np.mean(scores)) if scores else 0.5


def embedding_detector(answer, context):
    if not context.strip():
        return 0.5

    emb = ollama_embed([answer, context])
    return 1.0 - cosine_similarity(emb[0], emb[1])


def stochastic_detector(question, answer, context_chunks, n=3):
    if not context_chunks:
        return 0.5

    variants = [rag_answer(question, context_chunks) for _ in range(n)]
    embs = ollama_embed([answer] + variants)

    sims = [
        cosine_similarity(embs[0], embs[i])
        for i in range(1, len(embs))
    ]
    return 1.0 - float(np.mean(sims))


def token_overlap_detector(answer, context):
    if not context.strip():
        return 0.5

    overlap = SequenceMatcher(
        None,
        answer.lower().split(),
        context.lower().split()
    ).ratio()

    return 1.0 - overlap


# =========================
# MAIN AGGREGATOR
# =========================

def detect_hallucinations(question, answer, context_chunks):
    has_context = bool(context_chunks)
    context = "\n\n".join(context_chunks)

    if not has_context:
        return {
            "_meta": {
                "no_context": True,
                "warning": (
                    "Nie znaleziono fragmentu w dokumencie, "
                    "na podstawie którego można odpowiedzieć na pytanie."
                )
            },
            "llm": {
                "name": "Detektor LLM",
                "description": "Brak kontekstu — odpowiedź nie jest oparta na dokumencie.",
                "score": 0.5,
            },
            "embedding": {
                "name": "Detektor embeddingów",
                "description": "Brak kontekstu do porównania semantycznego.",
                "score": 0.5,
            },
            "stochastic": {
                "name": "Stochastic checker",
                "description": "Porównanie losowych wariantów bez odniesienia do dokumentu.",
                "score": 0.5,
            },
            "token": {
                "name": "Token similarity",
                "description": "Brak kontekstu — brak pokrycia tokenów.",
                "score": 0.5,
            },
        }

    return {
        "llm": {
            "name": "Detektor LLM",
            "description": "Model ocenia, czy odpowiedź jest oparta wyłącznie na kontekście.",
            "score": llm_detector(answer, context),
        },
        "embedding": {
            "name": "Detektor embeddingów",
            "description": "Porównanie semantyczne odpowiedzi i kontekstu.",
            "score": embedding_detector(answer, context),
        },
        "stochastic": {
            "name": "Stochastic checker",
            "description": "Stabilność odpowiedzi względem losowych generacji.",
            "score": stochastic_detector(question, answer, context_chunks),
        },
        "token": {
            "name": "Token similarity",
            "description": "Pokrycie tokenów odpowiedzi z kontekstem.",
            "score": token_overlap_detector(answer, context),
        },
    }
