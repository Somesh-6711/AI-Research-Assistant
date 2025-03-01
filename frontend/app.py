import streamlit as st
import os
from backend.summarization import answer_question, summarize_text
from backend.store_embeddings import search_papers
from utils.pdf_parser import extract_text_from_pdf
from utils.export_pdf import save_summary_as_pdf
from utils.topic_categorization import categorize_paper

# Apply custom CSS for styling
st.set_page_config(page_title="ज्ञानीका - AI Research Assistant", layout="wide")

# Dark/Light Mode Toggle
theme = st.sidebar.radio("🎨 Choose Theme:", ["Dark Mode", "Light Mode"])

if theme == "Dark Mode":
    st.markdown("<style>" + open("frontend/style.css").read() + "</style>", unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
        body {
            background-color: #F4F4F4;
            color: #000000;
        }
        .paper-card {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
        }
        .read-more {
            color: #007BFF;
        }
        button {
            background-color: #007BFF;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("📚 ज्ञानीका - AI-Powered Research Assistant")

# Sidebar for Query and File Upload
st.sidebar.header("🔎 Search & Ask")
query = st.sidebar.text_input("Enter your research query:")

if st.sidebar.button("Search Papers"):
    with st.spinner("Searching for relevant papers..."):
        results = search_papers(query, top_k=7)
        for idx, paper in enumerate(results, start=1):
            summary_text = paper.get('summary', 'No summary available')  # Default text if summary is missing
            category = categorize_paper(summary_text)

            st.markdown(f"""
                <div class='paper-card'>
                    <h4>{idx}. {paper['title']}</h4>
                    <p><b>📅 Published:</b> {paper['published']} | <b>📂 Category:</b> {category}</p>
                    <p><b>👨‍🔬 Authors:</b> {paper['authors']}</p>
                    <a href="{paper['link']}" target="_blank" class="read-more">🔗 Read More</a>
                </div>
            """, unsafe_allow_html=True)

            # PDF Export Button (Fixed)
            if summary_text != "No summary available":
                if st.button(f"📄 Export '{paper['title'][:30]}...' as PDF", key=f"export_{idx}"):
                    save_summary_as_pdf(paper['title'], summary_text)
                    st.success(f"✅ PDF saved for '{paper['title']}'!")

# Sidebar: Upload & Summarize PDFs
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

                # Export PDF Button
                if st.button(f"📄 Export Summary as PDF"):
                    save_summary_as_pdf(uploaded_file.name, summary)
                    st.success("✅ Summary exported as PDF!")

# Sidebar: AI Q&A
st.sidebar.header("💬 Ask AI a Question")
user_question = st.sidebar.text_area("Enter your question:")

if st.sidebar.button("Get Answer"):
    with st.spinner("Thinking..."):
        answer = answer_question(user_question)
        st.subheader("🤖 Response")
        st.write(answer)
