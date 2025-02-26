import requests
import xml.etree.ElementTree as ET

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_arxiv_papers(query: str, max_results: int = 5):
    """
    Fetch research papers from arXiv API based on a query.
    
    Args:
        query (str): The search query (e.g., "Machine Learning").
        max_results (int): Number of papers to fetch (default: 5).
    
    Returns:
        list[dict]: List of papers with title, summary, authors, and published date.
    """
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    
    response = requests.get(ARXIV_API_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch from arXiv API. Status Code: {response.status_code}")

    root = ET.fromstring(response.text)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
        link = entry.find("{http://www.w3.org/2005/Atom}id").text

        papers.append({
            "title": title,
            "summary": summary,
            "published": published,
            "authors": authors,
            "link": link
        })

    return papers

# Example usage
if __name__ == "__main__":
    query = "Machine Learning"
    results = fetch_arxiv_papers(query, max_results=3)
    for idx, paper in enumerate(results, start=1):
        print(f"{idx}. {paper['title']} ({paper['published']})")
        print(f"   Authors: {', '.join(paper['authors'])}")
        print(f"   Summary: {paper['summary'][:300]}...")  # Show first 300 chars
        print(f"   Link: {paper['link']}\n")
