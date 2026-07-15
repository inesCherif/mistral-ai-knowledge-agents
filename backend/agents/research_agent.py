import arxiv
from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import settings

def search_mistral_papers(max_results=5):
    client = arxiv.Client()
    search = arxiv.Search(
        query="all:Mistral AND all:AI OR all:Mixtral",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    try:
        for r in client.results(search):
            papers.append({
                "id": r.get_short_id(),
                "title": r.title,
                "summary": r.summary,
                "authors": [a.name for a in r.authors],
                "published": r.published.strftime("%Y-%m-%d"),
                "url": r.pdf_url,
                "type": "research"
            })
    except Exception as e:
        print(f"Error fetching from arxiv: {e}")
    return papers

def run_research_agent(query: str):
    if not settings.MISTRAL_API_KEY:
        return {"answer": "Mistral API key is missing. Please configure it in the .env file.", "sources": [], "agent_used": "research_agent"}

    llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=settings.MISTRAL_API_KEY)
    
    # Retrieve some recent papers
    papers = search_mistral_papers(max_results=3)
    
    context = ""
    sources = []
    
    for p in papers:
        context += f"Title: {p['title']}\nAuthors: {', '.join(p['authors'])}\nPublished: {p['published']}\nSummary: {p['summary']}\nURL: {p['url']}\n\n"
        sources.append({
            "type": "research",
            "title": p["title"],
            "url": p["url"]
        })
    
    prompt = PromptTemplate.from_template(
        "You are MistralBot, an expert on Mistral AI's research papers.\n"
        "Use the following context from recent arXiv papers about Mistral AI to answer the user's question.\n"
        "If you don't know the answer, use your general knowledge but prioritize the context.\n\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\nAnswer:"
    )
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "query": query})
    
    return {
        "answer": answer,
        "sources": sources,
        "agent_used": "research_agent"
    }
