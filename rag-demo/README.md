# RAG Demo with LangChain + vLLM

A simple Retrieval-Augmented Generation demo using LangChain for document processing and vLLM for inference.

## Architecture

Documents → Text Splitter → Embeddings → FAISS Vector Store ↓ User Query → Embedding → Similarity Search → Context ↓ Prompt + Context → vLLM → Response

## Components

- **Document Loader**: LangChain DirectoryLoader for text files
- **Text Splitter**: RecursiveCharacterTextSplitter (500 char chunks)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS (CPU)
- **LLM**: vLLM serving microsoft/phi-2

## Setup

```bash
cd rag-demo
python3 -m venv venv
source venv/bin/activate
pip install langchain langchain-community langchain-huggingface faiss-cpu pypdf sentence-transformers openai

Usage
Ensure vLLM is running on port 8000, then:

source venv/bin/activate
python rag_demo.py

## Sample Output
Q: How many days can I work remotely?
A: Employees may work remotely up to 3 days per week with manager approval.

Q: What is the 401k match percentage?
A: 401(k) matching is provided at 4% of salary.

Q: Can I use AI tools at work?
A: Yes, employees may use AI tools for work purposes with appropriate oversight.

## Interview Talking Points

RAG reduces hallucinations by grounding responses in retrieved documents
Embeddings convert text to vectors for semantic similarity search
Chunk size affects retrieval quality (too small = missing context, too large = noise)
FAISS provides fast similarity search for production use
This pattern scales to thousands of documents 
