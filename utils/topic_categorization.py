import re

# Predefined categories with keywords
CATEGORY_KEYWORDS = {
    "NLP": ["natural language processing", "nlp", "text analysis", "chatbot", "language model"],
    "Robotics": ["robot", "autonomous", "robotics", "motion planning"],
    "Medicine": ["clinical", "biomedical", "healthcare", "diagnosis", "medical"],
    "Machine Learning": ["deep learning", "neural network", "reinforcement learning", "supervised learning"],
    "Finance": ["stock market", "trading", "economic", "finance", "risk analysis"],
    "Computer Vision": ["image recognition", "object detection", "cnn", "vision model"],
}

def categorize_paper(summary: str):
    """
    Categorize a research paper based on its summary.
    
    Args:
        summary (str): The paper's summary text.
    
    Returns:
        str: The assigned category.
    """
    summary = summary.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(re.search(rf"\b{keyword}\b", summary) for keyword in keywords):
            return category
    
    return "General Research"  # Default category if no match found

# Example Usage
if __name__ == "__main__":
    test_summary = "This paper discusses deep learning models for autonomous robotics and motion planning."
    print(f"Category: {categorize_paper(test_summary)}")  # Expected: Robotics
