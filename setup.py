from setuptools import setup, find_packages

# Read requirements from file, ignoring '-e .' lines
def read_requirements():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("-e")]

setup(
    name="ai_research_assistant",
    version="1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Somesh Panchal",
    description="AI-Powered Multimodal Research Assistant using LLM and RAG",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
