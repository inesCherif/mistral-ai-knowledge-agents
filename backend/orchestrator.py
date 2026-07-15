from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
from langchain_mistralai import ChatMistralAI
from config import settings
import operator

class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    intent: str
    response: dict

def intent_router(state: GraphState):
    if not settings.MISTRAL_API_KEY:
        return {"intent": "site"}
        
    last_message = state["messages"][-1].content
    llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=settings.MISTRAL_API_KEY)
    
    prompt = f"""
    Categorize the following user query into exactly one of these categories: 'models', 'site', 'research', 'github', 'contacts', or 'web'.
    - models: Questions about Mistral 7B, Mixtral, Codestral, capabilities, context length, benchmarks.
    - research: Questions about Mistral's research papers on arxiv, publications.
    - github: Questions about Mistral's open source code, repositories, stars, inference code.
    - contacts: Questions about organization, leadership, social media, discord, emails, offices.
    - site: General questions about Mistral AI or its website.
    - web: Use this as a fallback if the question is about Mistral AI but requires real-time web search (e.g., recent news, what new models exist today, etc), or if the question is completely unrelated to Mistral AI (so the bot can decline it).
    
    Output ONLY the category word in lowercase.
    Query: {last_message}
    """
    res = llm.invoke(prompt)
    intent = res.content.strip().lower()
    
    if intent not in ['models', 'site', 'research', 'github', 'contacts', 'web']:
        intent = 'web' # fallback to web for unknown queries so it can gracefully decline or search

        
    return {"intent": intent}

def route_to_agent(state: GraphState):
    return state["intent"]

def call_models(state: GraphState):
    from agents.models_agent import run_models_agent
    res = run_models_agent(state["messages"][-1].content)
    return {"response": res}

def call_site(state: GraphState):
    from agents.site_agent import run_site_agent
    res = run_site_agent(state["messages"][-1].content)
    return {"response": res}

def call_research(state: GraphState):
    from agents.research_agent import run_research_agent
    res = run_research_agent(state["messages"][-1].content)
    return {"response": res}

def call_github(state: GraphState):
    from agents.github_agent import run_github_agent
    res = run_github_agent(state["messages"][-1].content)
    return {"response": res}

def call_contacts(state: GraphState):
    from agents.contact_agent import run_contact_agent
    res = run_contact_agent(state["messages"][-1].content)
    return {"response": res}

def call_web(state: GraphState):
    from agents.web_agent import run_web_agent
    res = run_web_agent(state["messages"][-1].content)
    return {"response": res}

def build_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("intent_classifier", intent_router)
    workflow.add_node("models", call_models)
    workflow.add_node("site", call_site)
    workflow.add_node("research", call_research)
    workflow.add_node("github", call_github)
    workflow.add_node("contacts", call_contacts)
    workflow.add_node("web", call_web)
    
    workflow.add_edge(START, "intent_classifier")
    workflow.add_conditional_edges(
        "intent_classifier",
        route_to_agent,
        {
            "models": "models",
            "site": "site",
            "research": "research",
            "github": "github",
            "contacts": "contacts",
            "web": "web"
        }
    )
    
    workflow.add_edge("models", END)
    workflow.add_edge("site", END)
    workflow.add_edge("research", END)
    workflow.add_edge("github", END)
    workflow.add_edge("contacts", END)
    workflow.add_edge("web", END)
    
    # Removing MemorySaver for now due to langgraph 0.1.9 KeyError bug
    app = workflow.compile()
    return app

# Singleton graph instance
app_graph = build_graph()
