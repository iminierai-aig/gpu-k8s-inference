#!/usr/bin/env python3
"""
RAG Demo with LangChain + vLLM
Demonstrates retrieval-augmented generation using local documents
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import os

# Configuration
DOCS_DIR = "./sample_docs"
VLLM_URL = "http://localhost:8000/v1"
MODEL = "microsoft/phi-2"

def load_and_split_documents():
    """Load documents and split into chunks"""
    print("Loading documents...")
    loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s)")
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

def create_vector_store(chunks):
    """Create FAISS vector store with embeddings"""
    print("Creating embeddings (this may take a moment)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("Vector store created")
    return vector_store, embeddings

def query_vllm(prompt):
    """Send query to vLLM"""
    client = OpenAI(base_url=VLLM_URL, api_key="not-needed")
    
    response = client.completions.create(
        model=MODEL,
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def rag_query(vector_store, question):
    """Perform RAG query"""
    # Retrieve relevant documents
    docs = vector_store.similarity_search(question, k=2)
    
    # Build context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create prompt with context
    prompt = f"""Use the following context to answer the question. If the answer is not in the context, say "I don't have information about that."

Context:
{context}

Question: {question}

Answer:"""
    
    # Get response from vLLM
    response = query_vllm(prompt)
    
    return response, docs

def main():
    print("=" * 50)
    print("RAG Demo with LangChain + vLLM")
    print("=" * 50)
    print()
    
    # Load and process documents
    chunks = load_and_split_documents()
    
    # Create vector store
    vector_store, embeddings = create_vector_store(chunks)
    
    # Test queries
    test_questions = [
        "How many days can I work remotely?",
        "What is the 401k match percentage?",
        "How much PTO do employees get?",
        "Can I use AI tools at work?"
    ]
    
    print()
    print("=" * 50)
    print("Running test queries...")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\nQ: {question}")
        answer, sources = rag_query(vector_store, question)
        print(f"A: {answer}")
        print(f"   (Retrieved from {len(sources)} chunks)")
    
    print()
    print("=" * 50)
    print("Interactive mode - type 'quit' to exit")
    print("=" * 50)
    
    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            break
        if not question:
            continue
            
        answer, sources = rag_query(vector_store, question)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
