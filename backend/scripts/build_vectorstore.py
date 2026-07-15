import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import settings

URLS = [
    "https://mistral.ai/",
    "https://mistral.ai/company/",
    "https://docs.mistral.ai/getting-started/models/",
    "https://docs.mistral.ai/capabilities/completion/",
    "https://docs.mistral.ai/capabilities/embeddings/",
    "https://mistral.ai/news/mistral-large-2407/",
    "https://mistral.ai/news/codestral/",
]

def build_vectorstore():
    print(f"Scraping Mistral AI website... Loading {len(URLS)} URLs")
    loader = WebBaseLoader(URLS)
    docs = loader.load()
    
    print(f"Loaded {len(docs)} documents. Chunking text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    print(f"Created {len(splits)} chunks. Generating embeddings using Mistral API...")
    if not settings.MISTRAL_API_KEY:
        print("ERROR: MISTRAL_API_KEY is not set. Cannot generate embeddings.")
        sys.exit(1)
        
    embeddings = MistralAIEmbeddings(mistral_api_key=settings.MISTRAL_API_KEY)
    
    print("Building FAISS VectorStore...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    os.makedirs("data/vectorstore", exist_ok=True)
    vectorstore.save_local("data/vectorstore")
    print("Vectorstore built and saved successfully to backend/data/vectorstore!")

if __name__ == "__main__":
    build_vectorstore()
