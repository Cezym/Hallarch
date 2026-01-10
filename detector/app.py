# # app.py
# import streamlit as st
# from backend import load_pdf, chunk_text, RAG, rag_answer, hallucination_risk

# st.set_page_config(page_title="RAG + Hallucination Detection", layout="wide")

# st.title("📄 RAG z detekcją halucynacji (Ollama)")

# uploaded = st.file_uploader("Wrzuć dokument PDF", type=["pdf"])

# if uploaded:
#     with open("temp.pdf", "wb") as f:
#         f.write(uploaded.read())

#     text = load_pdf("temp.pdf")
#     chunks = chunk_text(text)
#     rag = RAG(chunks)

#     question = st.text_input("Zadaj pytanie")

#     if question:
#         with st.spinner("Myślę..."):
#             context = rag.retrieve(question)
#             answer = rag_answer(question, context)
#             risk, score = hallucination_risk(answer, context)

#         st.subheader("🧠 Odpowiedź")
#         st.write(answer)

#         st.subheader("🚨 Detekcja halucynacji")
#         st.write(risk)
#         st.progress(int(min(float(score), 1.0) * 100))

#         with st.expander("📚 Użyty kontekst"):
#             for c in context:
#                 st.markdown(f"> {c}")

import os
import streamlit as st
from backend import load_pdf, chunk_text, RAG, rag_answer, hallucination_risk

st.set_page_config(page_title="RAG + Hallucination Detection", layout="wide")
st.title("📄 RAG z detekcją halucynacji (Ollama)")

# Inicjalizacja stanu sesji
if "chat_id" not in st.session_state:
    st.session_state.chat_id = 0
if "rag" not in st.session_state:
    st.session_state.rag = None
if "context" not in st.session_state:
    st.session_state.context = None
if "answer" not in st.session_state:
    st.session_state.answer = None
if "risk" not in st.session_state:
    st.session_state.risk = None
if "score" not in st.session_state:
    st.session_state.score = 0.0

# Przycisk: nowa konwersacja
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🆕 New chat"):
        for k in ["rag", "context", "answer", "risk", "score"]:
            st.session_state[k] = None
        try:
            os.remove("temp.pdf")
        except FileNotFoundError:
            pass
        st.session_state.chat_id += 1
        st.rerun()

uploaded = st.file_uploader("Wrzuć dokument PDF", type=["pdf"], key=f"uploader_{st.session_state.chat_id}")

if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.read())
    text = load_pdf("temp.pdf")
    chunks = chunk_text(text)
    st.session_state.rag = RAG(chunks)

# Formularz z przyciskiem wysyłania
with st.form(key=f"qa_form_{st.session_state.chat_id}", clear_on_submit=False):
    question = st.text_input("Zadaj pytanie", key=f"question_{st.session_state.chat_id}")
    send = st.form_submit_button("📨 Send")

if send:
    if not st.session_state.rag:
        st.warning("Najpierw wgraj dokument PDF.")
    elif question and question.strip():
        with st.spinner("Myślę..."):
            context = st.session_state.rag.retrieve(question)
            answer = rag_answer(question, context)
            risk, score = hallucination_risk(answer, context)
        st.session_state.context = context
        st.session_state.answer = answer
        st.session_state.risk = risk
        st.session_state.score = float(score)

if st.session_state.answer:
    st.subheader("🧠 Odpowiedź")
    st.write(st.session_state.answer)

    st.subheader("🚨 Detekcja halucynacji")
    st.write(st.session_state.risk)
    st.progress(int(max(0.0, min(float(st.session_state.score), 1.0)) * 100))

    with st.expander("📚 Użyty kontekst"):
        for c in (st.session_state.context or []):
            st.markdown(f"> {c}")