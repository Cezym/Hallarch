import requests
import numpy as np
from pypdf import PdfReader
import faiss  # type: ignore

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"


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
    data = response.json()
    return data["message"]["content"]


def ollama_embed(texts, model="nomic-embed-text"):
    # Akceptuje str lub listę str; zwraca macierz (N, D)
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
        vec = np.array(r.json()["embedding"], dtype=np.float32)
        vectors.append(vec)
    return np.vstack(vectors)


def _l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return x / norms


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages.append(txt)
    return "\n".join(pages)


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += max(1, chunk_size - overlap)
    return chunks


class RAG:
    def __init__(self, chunks):
        self.chunks = chunks
        if len(chunks) == 0:
            self.embeddings = np.zeros((0, 1), dtype=np.float32)
            self.index = None
            return

        self.embeddings = ollama_embed(self.chunks)  # (N, D)
        self.embeddings = _l2_normalize(self.embeddings)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings.astype(np.float32))


    def retrieve(self, question, k=2, min_sim=0.55):
        if not self.chunks or (self.embeddings.shape[0] == 0):
            return []

        q_emb = ollama_embed(question)
        q_emb = _l2_normalize(q_emb)

        if faiss is not None and self.index is not None:
            sims, idx = self.index.search(q_emb.astype(np.float32), k)
            sims = sims[0]
            idx = idx[0]
        else:
            sims = (self.embeddings @ q_emb[0].astype(np.float32))
            idx = np.argsort(-sims)[:k]

        selected = [self.chunks[i] for i, s in zip(idx, sims) if float(s) >= float(min_sim)]
        return selected


def rag_answer(question, context_chunks):
    context = "\n\n".join(context_chunks).strip()
    has_context = bool(context)


    if has_context:
        sys_prompt = (
            "Jesteś pomocnym asystentem AI. Odpowiadaj WYŁĄCZNIE na podstawie 'KONTEKSTU'. "
            "Nie używaj żadnej wiedzy ogólnej ani domysłów."
        )
        user_prompt = f"KONTEKST:\n{context}\n\nPYTANIE:\n{question}\n\n"
    else:
        
        # Brak dopasowanego kontekstu – odpowiedz krótko na podstawie wiedzy ogólnej
        sys_prompt = (
            "Jesteś pomocnym asystentem AI. Odpowiedz krótko na podstawie ogólnej wiedzy. "
            "Bądź zwięzły."
        )
        user_prompt = f"PYTANIE:\n{question}\n\n"

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return ollama_chat(messages)


def cosine_similarity(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def similarity_score(answer, context):
    emb = ollama_embed([answer, context])
    return float(cosine_similarity(emb[0], emb[1]))


def llm_judge(answer, context):
    if not context.strip():
        return 0.0  # brak kontekstu => odpowiedź spoza dokumentu

    messages = [
        {"role": "system", "content": "Oceń w skali 0-1, czy odpowiedź opiera się WYŁĄCZNIE na kontekście. Zwróć tylko liczbę."},
        {
            "role": "user",
            "content": f"""
KONTEKST:
{context}

ODPOWIEDŹ:
{answer}

0 = halucynacja lub informacje spoza kontekstu
1 = w pełni oparta na kontekście

Zwróć tylko liczbę z zakresu [0,1].
""",
        },
    ]
    score = ollama_chat(messages).strip()
    try:
        return float(score)
    except ValueError:
        return 0.0


def hallucination_risk(answer, context_chunks):
    context = "\n\n".join(context_chunks).strip()

    # Brak dopasowanego kontekstu – informujemy użytkownika o średnim ryzyku
    if not context:
        return "🟡 Średnie prawdopodobieństwo halucynacji (brak dopasowanego kontekstu; odpowiedź spoza dokumentu)", 0.5

    sim = similarity_score(answer, context)
    judge = llm_judge(answer, context)
    final = float(0.6 * judge + 0.4 * sim)

    if final > 0.75:
        return "🟢 Niskie prawdopodobieństwo halucynacji", final
    elif final > 0.5:
        return "🟡 Średnie prawdopodobieństwo halucynacji", final
    else:
        return "🔴 Wysokie prawdopodobieństwo halucynacji", final