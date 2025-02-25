import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "AI-Research-Assistant"

# Define folder structure
folders = [
    "data/raw/",  # Raw datasets & documents
    "data/processed/",  # Processed datasets
    "models/",  # Pre-trained models & fine-tuned models
    "embeddings/",  # FAISS / ChromaDB storage
    "backend/",  # Backend API (FastAPI/Flask)
    "frontend/",  # Streamlit/Gradio UI
    "utils/",  # Helper functions (PDF parser, embeddings, etc.)
    "config/",  # Configuration settings
    "research/",  # Jupyter notebooks for experiments
    "backend/apis/",  # API integrations
]

# Define initial files to create
files = [
    "backend/api.py",  # API handling file
    "backend/document_processing.py",  # PDF and text processing functions
    "backend/retrieval.py",  # FAISS/ChromaDB search implementation
    "backend/summarization.py",  # LLM-based summarization
    "backend/apis/arxiv_api.py",  # arXiv API integration
    "frontend/app.py",  # Streamlit/Gradio UI main script
    "utils/pdf_parser.py",  # Extract text from PDFs
    "utils/web_scraper.py",  # Scrape text from web URLs
    "config/config.yaml",  # Configurations like API keys, paths, and options
    "requirements.txt",  # Dependencies
    "README.md",  # Project documentation
    "research/experiments.ipynb",  # Jupyter notebook for testing models
    "Dockerfile",  # Deployment setup
    "setup.py",  # Project setup file
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    logging.info(f"Created folder: {folder}")

# Create files
for file in files:
    file_path = Path(file)
    if not file_path.exists():
        with open(file_path, 'w') as f:
            f.write("")  # Create an empty file
        logging.info(f"Created file: {file}")
    else:
        logging.info(f"File already exists: {file}")
