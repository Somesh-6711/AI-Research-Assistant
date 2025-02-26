import chromadb
from sentence_transformers import SentenceTransformer
from apis.arxiv_api import fetch_arxiv_papers


# Load a pre-trained sentence embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight & fast

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="embeddings/")  # Saves embeddings persistently
collection = chroma_client.get_or_create_collection(name="research_papers")

def store_papers(query: str, max_results: int = 5):
    """
    Fetch papers from arXiv, generate embeddings, and store them in ChromaDB.
    """
    papers = fetch_arxiv_papers(query, max_results)

    for paper in papers:
        paper_text = f"{paper['title']} - {paper['summary']}"
        embedding = embedding_model.encode(paper_text).tolist()  # Convert to list for ChromaDB storage

        collection.add(
            ids=[paper["link"]],  # Use arXiv link as a unique ID
            embeddings=[embedding],
            metadatas=[{
                "title": paper["title"],
                "authors": ", ".join(paper["authors"]),
                "published": paper["published"],
                "link": paper["link"]
            }]
        )
    
    print(f"✅ {len(papers)} papers stored in ChromaDB!")

def search_papers(user_query: str, top_k: int = 3):
    """
    Search stored research papers using semantic similarity.
    """
    query_embedding = embedding_model.encode(user_query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Print search results
    for idx, doc in enumerate(results["metadatas"][0], start=1):
        print(f"{idx}. {doc['title']} ({doc['published']})")
        print(f"   Authors: {doc['authors']}")
        print(f"   Link: {doc['link']}\n")

# Example Usage
if __name__ == "__main__":
    store_papers("Machine Learning", max_results=5)  # Store 5 papers
    search_papers("deep learning models", top_k=3)  # Search papers based on query
