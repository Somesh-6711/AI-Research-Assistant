import streamlit as st
import os
from backend.summarization import answer_question, summarize_text
from backend.store_embeddings import search_papers
from utils.pdf_parser import extract_text_from_pdf

# Streamlit UI Setup
st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("📚 AI-Powered Multimodal Research Assistant")

# Sidebar for Query and File Upload
st.sidebar.header("🔎 Search & Ask")
query = st.sidebar.text_input("Enter your research query:")
if st.sidebar.button("Search Papers"):
    with st.spinner("Searching for relevant papers..."):
        results = search_papers(query, top_k=3)
        for idx, paper in enumerate(results, start=1):
            st.subheader(f"{idx}. {paper['title']}")
            st.write(f"📅 Published: {paper['published']}")
            st.write(f"👨‍🔬 Authors: {paper['authors']}")
            st.write(f"🔗 [Read More]({paper['link']})")
            st.write("---")

st.sidebar.header("📂 Upload a Research Paper")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Text from PDF")
        st.text_area("📄 Document Content:", pdf_text[:1000], height=200)  # Display first 1000 characters

        if st.button("Summarize PDF"):
            with st.spinner("Generating summary..."):
                summary = summarize_text(pdf_text)
                st.subheader("📜 AI-Generated Summary")
                st.write(summary)

st.sidebar.header("💬 Ask AI a Question")
user_question = st.sidebar.text_area("Enter your question:")
if st.sidebar.button("Get Answer"):
    with st.spinner("Thinking..."):
        answer = answer_question(user_question)
        st.subheader("🤖 AI Response")
        st.write(answer)
