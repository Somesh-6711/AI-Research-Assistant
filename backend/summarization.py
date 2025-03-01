import yaml
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from backend.store_embeddings import search_papers

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

OPENAI_API_KEY = config["openai_api_key"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def summarize_text(text: str):
    """
    Generate a concise summary of the given text using GPT.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following research paper in a concise way."},
            {"role": "user", "content": text}
        ]
    )
    
    return response.choices[0].message.content

def answer_question(query: str):
    """
    Retrieve relevant papers and generate an answer using OpenAI GPT.
    """
    relevant_papers = search_papers(query, top_k=3)

    # Ensure 'summary' exists, else use a placeholder
    context = "\n\n".join([
        f"Title: {p.get('title', 'Unknown Title')}\nSummary: {p.get('summary', 'No summary available')}" 
        for p in relevant_papers
    ])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer based on the following research papers."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    test_query = "What are the recent advancements in machine learning?"
    print(f"🔎 Question: {test_query}\n")
    
    answer = answer_question(test_query)
    print(f"🤖 AI Answer:\n{answer}\n")

    paper_text = "Machine Learning for Clinical Predictive Analytics - This paper discusses how ML is used in clinical predictions..."
    print("📜 TL;DR Summary:", summarize_text(paper_text))
