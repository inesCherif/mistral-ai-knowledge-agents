from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rag.vectorstore import get_retriever
from config import settings

def run_models_agent(query: str):
    if not settings.MISTRAL_API_KEY:
        return {"answer": "Mistral API key is missing. Please configure it in the .env file.", "sources": [], "agent_used": "models_agent"}

    llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=settings.MISTRAL_API_KEY)
    retriever = get_retriever()
    
    context = ""
    sources = []
    
    if retriever:
        docs = retriever.invoke(query)
        context = "\n\n".join([f"Source: {d.metadata.get('source', 'Unknown')}\n{d.page_content}" for d in docs])
        seen = set()
        for d in docs:
            url = d.metadata.get('source', 'Mistral Docs')
            if url not in seen and "docs.mistral.ai" in url:
                seen.add(url)
                sources.append({
                    "type": "model",
                    "title": url.split('/')[-2].replace('-', ' ').title() if url.endswith('/') else url.split('/')[-1].replace('-', ' ').title() or "Models Guide",
                    "url": url
                })
    
    prompt = PromptTemplate.from_template(
        "You are MistralBot, an expert on Mistral AI's models (Mistral 7B, Mixtral 8x7B, Mistral Large, Codestral, Mathstral, etc.).\n"
        "Use the following context retrieved from Mistral's documentation to answer the user's question.\n"
        "Give specific details like context length, parameter size, performance benchmarks, architecture, or API endpoint if applicable and present in the context.\n"
        "If you don't know the answer, use your general knowledge but prioritize the context.\n\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\nAnswer:"
    )
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "query": query})
    
    return {
        "answer": answer,
        "sources": sources,
        "agent_used": "models_agent"
    }
