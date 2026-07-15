"""
MistralBot Orchestrator — Simple intent-based router.
Replaces LangGraph StateGraph (which has a known bug in v0.1.9).
Does the same thing: classify intent → route to the right agent.
"""
from langchain_mistralai import ChatMistralAI
from config import settings


def classify_intent(query: str) -> str:
    """Use Mistral LLM to classify the user query into one of 6 intents."""
    if not settings.MISTRAL_API_KEY:
        return "site"

    llm = ChatMistralAI(
        model="mistral-large-latest",
        mistral_api_key=settings.MISTRAL_API_KEY
    )

    prompt = f"""Categorize the following user query into exactly one of these categories:
'models', 'site', 'research', 'github', 'contacts', or 'web'.

- models: Questions about Mistral 7B, Mixtral, Codestral, capabilities, context length, benchmarks, API pricing.
- research: Questions about Mistral's research papers on arxiv, publications, academic work.
- github: Questions about Mistral's open source code, repositories, stars, inference code.
- contacts: Questions about organization, leadership, team members, social media, discord, emails, offices.
- site: General questions about Mistral AI company, products, pricing, news, website.
- web: Use this ONLY when the question is about very recent real-time Mistral news/updates not in existing knowledge, OR if it is completely unrelated to Mistral AI.

Output ONLY the single category word in lowercase, nothing else.
Query: {query}"""

    try:
        res = llm.invoke(prompt)
        intent = res.content.strip().lower()
        if intent not in ['models', 'site', 'research', 'github', 'contacts', 'web']:
            intent = 'site'
        return intent
    except Exception as e:
        print(f"Intent classification failed: {e}")
        return 'site'


def run_orchestrator(query: str) -> dict:
    """Main entry point. Classify intent and dispatch to the correct agent."""
    intent = classify_intent(query)

    try:
        if intent == "models":
            from agents.models_agent import run_models_agent
            result = run_models_agent(query)

        elif intent == "research":
            from agents.research_agent import run_research_agent
            result = run_research_agent(query)

        elif intent == "github":
            from agents.github_agent import run_github_agent
            result = run_github_agent(query)

        elif intent == "contacts":
            from agents.contact_agent import run_contact_agent
            result = run_contact_agent(query)

        elif intent == "web":
            from agents.web_agent import run_web_agent
            result = run_web_agent(query)

        else:  # site (default)
            from agents.site_agent import run_site_agent
            result = run_site_agent(query)

    except Exception as e:
        print(f"Agent execution failed for intent '{intent}': {e}")
        result = {
            "answer": f"I encountered an error while processing your question. Please try again.",
            "sources": [],
            "agent_used": "error_handler"
        }

    result["intent"] = intent
    return result
