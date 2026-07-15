import os
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from config import settings

_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore
        
    if not settings.MISTRAL_API_KEY:
        return None
        
    vs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'vectorstore'))
    if os.path.exists(vs_path):
        embeddings = MistralAIEmbeddings(mistral_api_key=settings.MISTRAL_API_KEY)
        _vectorstore = FAISS.load_local(vs_path, embeddings, allow_dangerous_deserialization=True)
        return _vectorstore
    return None

def get_retriever(k=4):
    vs = get_vectorstore()
    if vs:
        return vs.as_retriever(search_kwargs={"k": k})
    return None
