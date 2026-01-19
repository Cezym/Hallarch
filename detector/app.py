"""
## System RAG z detekcją halucynacji

Celem systemu jest wykrywanie potencjalnych halucynacji w odpowiedziach generowanych przez model językowy 
w architekturze RAG. 
System implementuje cztery niezależne metody detekcji:


1. LLM-based Judge (detektor oparty na LLM)


Metoda wykorzystuje duży model językowy jako sędziego semantycznego, który ocenia, 
czy odpowiedź została wygenerowana wyłącznie na podstawie dostarczonego kontekstu.


1. Kontekst i odpowiedź są przekazywane do LLM w postaci promptu oceniającego.
2. Model otrzymuje instrukcję zwrócenia **pojedynczej liczby z zakresu [0,1]**:

   * `0.0` – odpowiedź całkowicie spoza kontekstu (halucynacja)
   * `1.0` – odpowiedź w pełni oparta na kontekście
3. W praktyce wynik jest interpretowany jako **confidence score zgodności z kontekstem**.



Zalety:

* Bardzo dobra ocena semantyczna i logiczna
* Radzi sobie z parafrazami i implikacjami
* Najlepsza metoda do wykrywania subtelnych halucynacji

Wady / fałszywe alarmy:
* Metoda niestabilna (zależna od promptu)
* Wrażliwa na bias samego LLM

----------------------------------------------------------------
----------------------------------------------------------------

2. Semantic Similarity Detector (embedding-based)

Metoda opiera się na założeniu, że odpowiedź oparta na kontekście powinna być semantycznie podobna do 
tego kontekstu w przestrzeni embeddingów.

1.Obliczane są embeddingi: E_answer, E_context
2. Obliczana jest cosinusowa miara podobieństwa: sim = cosine_similarity(E_answer, E_context)
3.Wynik jest mapowany na prawdopodobieństwo halucynacji: hallucination_score = 1 - sim
    Zakres
    sim → 1.0 → niskie ryzyko halucynacji
    sim → 0.0 → wysokie ryzyko halucynacji

Zalety:
*Szybka i deterministyczna
*Dobrze działa przy długich fragmentach
Łatwa do skalowania

Wady / fałszywe alarmy:
*Może fałszywie alarmować przy krótkich odpowiedziach
*Nie wykrywa logicznych sprzeczności
*Wrażliwa na "rozmycie" embeddingu przy dużych chunkach

----------------------------------------------------------------
----------------------------------------------------------------
3. Stochastic Consistency Checker (BERT stochastic checker)

Metoda bada stabilność odpowiedzi modelu przy wielokrotnym generowaniu odpowiedzi z losowością (temperature > 0).

Założenie: halucynacje są niestabilne semantycznie i zmieniają się między próbkami.

1.Generowanych jest N odpowiedzi (N ≥ 3) z losowością.
2.Każda para odpowiedzi jest porównywana za pomocą metryki BERTScore.
3.Obliczana jest średnia spójność semantyczna: consistency = mean(BERTScore(answer_i, answer_j))

Interpretacja:
Wysoka spójność → odpowiedź stabilna
Niska spójność → możliwa halucynacja

Zalety:
*Dobrze wykrywa "wymyślane" fakty
*Niezależna od jawnego kontekstu

Wady / fałszywe alarmy:
*Bardzo kosztowna obliczeniowo
*Może fałszywie alarmować przy pytaniach otwartych
*Wymaga wielu wywołań modelu


----------------------------------------------------------------
----------------------------------------------------------------

4. Token Similarity Detector (lexical overlap)

Najprostsza metoda, oparta na pokryciu leksykalnym między odpowiedzią a kontekstem.


Algorytm:
1.Tokenizacja odpowiedzi i kontekstu
2.Obliczenie pokrycia tokenów: coverage = |tokens_answer ∩ tokens_context| / |tokens_answer|

Score halucynacji:
hallucination_score = 1 - coverage

Interpretacja
coverage → 1.0 → odpowiedź oparta na kontekście
coverage → 0.0 → odpowiedź spoza kontekstu

Zalety:
*Bardzo szybka

Wady / fałszywe alarmy:
*Bardzo wrażliwa na parafrazy
*Nie działa dobrze dla synonimów
*Może fałszywie alarmować przy streszczeniach

----------------------------------------------------------------
----------------------------------------------------------------


"""







import os
import streamlit as st

from backend import (
    load_pdf,
    chunk_text,
    RAG,
    rag_answer,
    detect_hallucinations,
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="RAG + Hallucination Detection",
    layout="wide",
)

st.title("📄 RAG z detekcją halucynacji (Ollama)")

# =========================
# SESSION STATE
# =========================

for key in ["chat_id", "rag", "context", "answer", "hallucinations"]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state.chat_id is None:
    st.session_state.chat_id = 0


# =========================
# NEW CHAT
# =========================

if st.button("🆕 New chat"):
    for k in ["rag", "context", "answer", "hallucinations"]:
        st.session_state[k] = None
    try:
        os.remove("temp.pdf")
    except FileNotFoundError:
        pass
    st.session_state.chat_id += 1
    st.rerun()


# =========================
# PDF UPLOAD
# =========================

uploaded = st.file_uploader(
    "Wrzuć dokument PDF",
    type=["pdf"],
    key=f"uploader_{st.session_state.chat_id}",
)

if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.read())

    text = load_pdf("temp.pdf")
    chunks = chunk_text(text)
    st.session_state.rag = RAG(chunks)
    st.success(f"📑 Załadowano dokument ({len(chunks)} fragmentów)")


# =========================
# QUESTION FORM
# =========================

with st.form(key=f"qa_form_{st.session_state.chat_id}"):
    question = st.text_input(
        "Zadaj pytanie",
        key=f"question_{st.session_state.chat_id}",
    )
    send = st.form_submit_button("📨 Send")


# =========================
# RAG PIPELINE
# =========================

if send:
    if not st.session_state.rag:
        st.warning("Najpierw wgraj dokument PDF.")
    elif question and question.strip():
        with st.spinner("Myślę..."):
            context = st.session_state.rag.retrieve(question)
            answer = rag_answer(question, context)
            hallucinations = detect_hallucinations(
                question, answer, context
            )

        st.session_state.context = context
        st.session_state.answer = answer
        st.session_state.hallucinations = hallucinations


# =========================
# ANSWER + WARNINGS
# =========================

if st.session_state.answer:
    st.subheader("🧠 Odpowiedź")
    st.write(st.session_state.answer)

    meta = st.session_state.hallucinations.get("_meta")
    if meta and meta.get("no_context"):
        st.warning("⚠️ " + meta["warning"])

    st.subheader("🚨 Detekcja halucynacji")

    for key, det in st.session_state.hallucinations.items():
        if key == "_meta":
            continue

        score = float(det["score"])

        st.markdown(f"### {det['name']}")
        st.caption(det["description"])
        st.progress(int(score * 100))
        st.write(f"Prawdopodobieństwo halucynacji: **{score:.2f}**")

        if score < 0.33:
            st.success("Niskie ryzyko halucynacji")
        elif score < 0.66:
            st.warning("Średnie ryzyko halucynacji")
        else:
            st.error("Wysokie ryzyko halucynacji")

        st.divider()


# =========================
# CONTEXT VIEW
# =========================

if st.session_state.context:
    with st.expander("📚 Użyty kontekst"):
        for c in st.session_state.context:
            st.markdown(f"> {c}")
