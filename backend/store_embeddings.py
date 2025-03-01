import chromadb
from sentence_transformers import SentenceTransformer
from backend.apis.arxiv_api import fetch_arxiv_papers

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
        # Ensure summary exists
        paper_summary = paper.get("summary", "").strip()
        if not paper_summary:
            paper_summary = "No summary available."

        paper_text = f"{paper['title']} - {paper_summary}"
        embedding = embedding_model.encode(paper_text).tolist()  # Convert to list for ChromaDB storage

        collection.add(
            ids=[paper["link"]],  # Use arXiv link as a unique ID
            embeddings=[embedding],
            metadatas=[{
                "title": paper["title"],
                "summary": paper_summary,  # Ensure summary is always stored
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

    # Ensure we return results properly
    if not results or "metadatas" not in results or not results["metadatas"][0]:
        print("⚠️ No relevant papers found.")
        return []

    return results["metadatas"][0]  # Return a list of metadata

# Example Usage
if __name__ == "__main__":
    store_papers("Machine Learning", max_results=5)  # Store 5 papers
    search_results = search_papers("deep learning models", top_k=3)
    
    if search_results:
        print("\n🔍 Retrieved Papers:")
        for idx, doc in enumerate(search_results, start=1):
            print(f"{idx}. {doc['title']} ({doc['published']})")
            print(f"   Authors: {doc['authors']}")
            print(f"   Link: {doc['link']}\n")
