from github import Github
from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import settings

def search_mistral_repos():
    # Authenticated or unauthenticated Github client
    g = Github(settings.GITHUB_TOKEN) if settings.GITHUB_TOKEN and settings.GITHUB_TOKEN != "your_github_token_here" else Github()
    repos = []
    try:
        org = g.get_organization("mistralai")
        # Get top repos by stars
        org_repos = sorted(list(org.get_repos()), key=lambda x: x.stargazers_count, reverse=True)
        for repo in org_repos[:6]: 
            lic = repo.license.name if repo.license else "Unknown"
            repos.append({
                "id": str(repo.id),
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description or "No description provided.",
                "stars": repo.stargazers_count,
                "url": repo.html_url,
                "language": repo.language or "Unknown",
                "forks": repo.forks_count,
                "topics": repo.get_topics(),
                "last_updated": repo.updated_at.strftime("%Y-%m-%d") if repo.updated_at else "",
                "open_issues": repo.open_issues_count,
                "license": lic
            })
    except Exception as e:
        print(f"Error fetching from GitHub: {e}")
    return repos

def run_github_agent(query: str):
    if not settings.MISTRAL_API_KEY:
        return {"answer": "Mistral API key is missing. Please configure it in the .env file.", "sources": [], "agent_used": "github_agent"}

    llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=settings.MISTRAL_API_KEY)
    
    repos = search_mistral_repos()
    
    context = ""
    sources = []
    
    for r in repos:
        context += f"Repo: {r['name']}\nDescription: {r['description']}\nStars: {r['stars']}\nLanguage: {r['language']}\nURL: {r['url']}\n\n"
        sources.append({
            "type": "github",
            "title": r["name"],
            "url": r["url"]
        })
    
    prompt = PromptTemplate.from_template(
        "You are MistralBot, an expert on Mistral AI's open-source GitHub repositories.\n"
        "Use the following context from MistralAI's official GitHub to answer the user's question.\n"
        "If you don't know the answer, use your general knowledge but prioritize the context.\n\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\nAnswer:"
    )
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "query": query})
    
    return {
        "answer": answer,
        "sources": sources,
        "agent_used": "github_agent"
    }
