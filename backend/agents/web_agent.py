from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import settings
from tavily import TavilyClient

def search_web(query: str):
    if not settings.TAVILY_API_KEY or settings.TAVILY_API_KEY == "your_tavily_api_key_here":
        print("Tavily API key is missing or default.")
        return []
    try:
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        # Always append Mistral AI to force relevant search results
        search_query = f"Mistral AI {query}"
        response = client.search(search_query, search_depth="basic", max_results=3)
        return response.get("results", [])
    except Exception as e:
        print(f"Tavily search failed: {e}")
        return []

def run_web_agent(query: str):
    if not settings.MISTRAL_API_KEY:
        return {"answer": "Mistral API key is missing.", "sources": [], "agent_used": "web_agent"}
        
    llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=settings.MISTRAL_API_KEY)
    
    results = search_web(query)
    
    context = ""
    sources = []
    
    for r in results:
        context += f"Source: {r.get('title', 'Web Page')}\nContent: {r.get('content', '')}\nURL: {r.get('url', '')}\n\n"
        sources.append({
            "type": "web",
            "title": r.get("title", "Web Result")[:30] + "...",
            "url": r.get("url", "")
        })
        
    if not context:
        prompt_fallback = PromptTemplate.from_template(
            "You are MistralBot. You ONLY answer questions about Mistral AI.\n"
            "If the question is unrelated to Mistral AI, politely decline.\n"
            "Question: {query}\nAnswer:"
        )
        chain_fb = prompt_fallback | llm | StrOutputParser()
        answer = chain_fb.invoke({"query": query})
        return {
            "answer": answer,
            "sources": [],
            "agent_used": "web_agent"
        }
    
    prompt = PromptTemplate.from_template(
        "You are MistralBot, an AI assistant dedicated ONLY to Mistral AI.\n"
        "The user's question couldn't be answered by your internal database, so we searched the web.\n"
        "If the user's question is completely unrelated to Mistral AI, politely decline to answer.\n"
        "Otherwise, use the following real-time web search results to answer the user's question.\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\nAnswer:"
    )
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "query": query})
    
    return {
        "answer": answer,
        "sources": sources,
        "agent_used": "web_agent"
    }
