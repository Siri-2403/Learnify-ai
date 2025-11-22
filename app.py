import streamlit as st
from helpers.summarize import generate_summary
from helpers.quiz import generate_quiz
from helpers.rag_faiss import answer_with_faiss
from helpers.pdf_reader import extract_text_from_pdf
from helpers.ocr import extract_text_from_image

if "history" not in st.session_state:
    st.session_state.history = []

def save_to_history(title, content):
    st.session_state.history.append({
        "title": title,
        "content": content
    })

st.set_page_config(page_title="Learnify AI", page_icon="📚")

with st.sidebar:
    st.header("⚙️ Options")

    if st.button("🔄 New Chat"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("### 📝 My Notes")

    if st.session_state.history:
        for item in st.session_state.history:
            with st.expander(item["title"]):
                st.write(item["content"])
    else:
        st.write("No notes saved yet.")

st.title("📚 Learnify AI — Your Smart Study Assistant")

col1, col2 = st.columns(2)

with col1:
    uploaded_pdf = st.file_uploader("📄 Upload PDF", type=["pdf"])

with col2:
    uploaded_image = st.file_uploader("🖼️ Upload Image", type=["jpg", "jpeg", "png"])


extracted_text = ""

if uploaded_pdf is not None:
    status = st.empty()
    status.info("⏳ Extracting text from PDF… please wait")
    with st.spinner("Reading PDF…"):
        extracted_text += extract_text_from_pdf(uploaded_pdf) + "\n"
    status.success("✅ PDF text extracted successfully!")

if uploaded_image is not None:
    status = st.empty()
    status.info("⏳ Extracting text from handwritten image… please wait")
    with st.spinner("Running OCR…"):
        extracted_text += extract_text_from_image(uploaded_image) + "\n"
    status.success("✅ Image text extracted successfully!")

final_notes = st.text_area("Your combined study notes (editable):", extracted_text, height=300)

if st.button("Generate Summary"):
    if final_notes.strip():
        with st.spinner("⏳ Generating summary…"):
            summary = generate_summary(final_notes)
        st.subheader("📄 Summary")
        st.write(summary)
        st.download_button("Download Summary", summary, "summary.txt")
        save_to_history("Summary", summary)
    else:
        st.error("Please upload or type some notes.")

if st.button("Generate Quiz"):
    if final_notes.strip():
        with st.spinner("⏳ Generating quiz…"):
            quiz = generate_quiz(final_notes)
        st.subheader("📝 Quiz")
        st.write(quiz)
        st.download_button("Download Quiz", quiz, "quiz.txt")
        save_to_history("Quiz", quiz)
    else:
        st.error("Please upload or type some notes.")

question = st.text_input("Ask a doubt:")

if st.button("Solve Doubt"):
    if final_notes.strip() and question.strip():
        with st.spinner("⏳ Thinking…"):
            answer = answer_with_faiss(final_notes, question)
        st.subheader("💡 Answer (RAG)")
        st.write(answer)
        st.download_button("Download Answer", answer, "answer.txt")
        save_to_history("Answer", answer)
    else:
        st.error("Please enter notes and a question.")
