"""
Chat Router — Phase 1: Mock responses with intent detection skeleton
Phase 2+: Will connect to LangGraph orchestrator
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import time

router = APIRouter()


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = []


class Source(BaseModel):
    type: str          # "site" | "model" | "paper" | "github" | "contact"
    title: str
    url: Optional[str] = None
    excerpt: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    intent: str
    agent_used: str
    sources: List[Source] = []
    conversation_id: str
    response_time_ms: int


def detect_intent(message: str) -> str:
    """Simple keyword-based intent detection (Phase 1 mock)."""
    msg = message.lower()
    if any(k in msg for k in ["model", "mixtral", "mistral 7b", "large", "codestral", "embed"]):
        return "models"
    if any(k in msg for k in ["paper", "research", "arxiv", "benchmark", "mmlu", "humaneval"]):
        return "research"
    if any(k in msg for k in ["github", "repo", "code", "implementation", "notebook"]):
        return "github"
    if any(k in msg for k in ["contact", "who", "team", "ceo", "founder", "linkedin", "email", "person"]):
        return "contacts"
    return "site"


MOCK_RESPONSES = {
    "models": {
        "answer": (
            "Mistral AI offers several powerful models:\n\n"
            "• **Mistral 7B** — The original 7B parameter model, Apache 2.0 licensed, "
            "outperforms Llama 2 13B on many benchmarks.\n"
            "• **Mixtral 8x7B** — A Mixture of Experts (MoE) model with 8 experts of 7B each, "
            "matching GPT-3.5 performance.\n"
            "• **Mistral Large** — Top-tier model for complex reasoning tasks, available via API.\n"
            "• **Codestral** — Specialized for code generation (80+ languages).\n"
            "• **Mistral Embed** — Text embedding model for RAG applications.\n\n"
            "All models are accessible via the Mistral API at `api.mistral.ai`."
        ),
        "agent_used": "models_agent",
        "sources": [
            Source(type="site", title="Mistral AI Models", url="https://mistral.ai/models"),
            Source(type="site", title="Mistral API Docs", url="https://docs.mistral.ai"),
        ],
    },
    "research": {
        "answer": (
            "Key Mistral AI research papers:\n\n"
            "• **Mistral 7B** (Jiang et al., 2023) — Introduces Grouped Query Attention (GQA) "
            "and Sliding Window Attention (SWA). Beats Llama 2 on all benchmarks.\n"
            "• **Mixtral of Experts** (Jiang et al., 2024) — MoE architecture, 45B total params "
            "but only 12B active per token.\n\n"
            "**Benchmark highlights (Mistral 7B)**:\n"
            "| Benchmark | Mistral 7B | Llama 2 13B |\n"
            "|-----------|-----------|-------------|\n"
            "| MMLU | 60.1 | 54.8 |\n"
            "| HumanEval | 30.5 | 18.3 |\n"
            "| GSM8K | 52.2 | 28.7 |"
        ),
        "agent_used": "research_agent",
        "sources": [
            Source(type="paper", title="Mistral 7B (arXiv:2310.06825)", url="https://arxiv.org/abs/2310.06825"),
            Source(type="paper", title="Mixtral of Experts (arXiv:2401.04088)", url="https://arxiv.org/abs/2401.04088"),
        ],
    },
    "github": {
        "answer": (
            "Mistral AI's main GitHub organization is **mistralai** with these key repos:\n\n"
            "• **mistral-src** — Reference implementation of Mistral models (Python)\n"
            "• **mistral-inference** — Fast inference engine for Mistral models\n"
            "• **mistral-finetune** — Fine-tuning scripts for Mistral models\n"
            "• **mistral-common** — Shared utilities (tokenizer, etc.)\n"
            "• **client-python** — Official Python client for the Mistral API\n"
            "• **client-js** — Official JavaScript client for the Mistral API\n\n"
            "GitHub org: https://github.com/mistralai"
        ),
        "agent_used": "github_agent",
        "sources": [
            Source(type="github", title="mistralai GitHub", url="https://github.com/mistralai"),
            Source(type="github", title="mistral-src", url="https://github.com/mistralai/mistral-src"),
        ],
    },
    "contacts": {
        "answer": (
            "**Mistral AI Key Team Members:**\n\n"
            "• **Arthur Mensch** — CEO & Co-founder. Former DeepMind researcher.\n"
            "  LinkedIn: linkedin.com/in/arthur-mensch\n\n"
            "• **Guillaume Lample** — Co-founder, Research Lead. Ex-Meta AI (LLaMA author).\n"
            "  LinkedIn: linkedin.com/in/guillaume-lample\n\n"
            "• **Timothée Lacroix** — Co-founder, CTO. Ex-Meta AI.\n"
            "  LinkedIn: linkedin.com/in/timothee-lacroix\n\n"
            "• **Sophia Yang** — Head of Developer Relations.\n"
            "  Twitter/X: @sophiamyang\n\n"
            "**Official Contact:**\n"
            "• Press: press@mistral.ai\n"
            "• Enterprise: enterprise@mistral.ai\n"
            "• Discord: discord.gg/mistralai\n"
            "• Twitter/X: @MistralAI"
        ),
        "agent_used": "contact_agent",
        "sources": [
            Source(type="contact", title="Mistral AI Team", url="https://mistral.ai/company"),
            Source(type="contact", title="Arthur Mensch — LinkedIn", url="https://linkedin.com/in/arthur-mensch"),
        ],
    },
    "site": {
        "answer": (
            "**Mistral AI** is a French AI startup founded in April 2023 by former DeepMind and Meta AI researchers. "
            "Based in Paris, France, it has quickly become one of Europe's leading AI companies.\n\n"
            "**Key facts:**\n"
            "• Founded: April 2023\n"
            "• HQ: Paris, France\n"
            "• Valuation: ~$6 billion (2024)\n"
            "• Mission: Open, efficient, and responsible frontier AI\n"
            "• Products: API platform, La Plateforme, Le Chat (consumer chatbot)\n\n"
            "**Links:**\n"
            "• Website: https://mistral.ai\n"
            "• API Console: https://console.mistral.ai\n"
            "• Le Chat: https://chat.mistral.ai"
        ),
        "agent_used": "site_agent",
        "sources": [
            Source(type="site", title="Mistral AI Website", url="https://mistral.ai"),
            Source(type="site", title="About Mistral AI", url="https://mistral.ai/company"),
        ],
    },
}


from agents.models_agent import run_models_agent
from agents.site_agent import run_site_agent
from agents.research_agent import run_research_agent

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    start = time.time()
    intent = detect_intent(request.message)
    
    if intent == "models":
        res = run_models_agent(request.message)
        answer = res["answer"]
        agent_used = res["agent_used"]
        sources = res["sources"]
    elif intent == "site":
        res = run_site_agent(request.message)
        answer = res["answer"]
        agent_used = res["agent_used"]
        sources = res["sources"]
    elif intent == "research":
        res = run_research_agent(request.message)
        answer = res["answer"]
        agent_used = res["agent_used"]
        sources = res["sources"]
    else:
        # Fallback to mock for phases 4-5
        mock = MOCK_RESPONSES.get(intent, MOCK_RESPONSES["site"])
        answer = mock["answer"]
        agent_used = mock["agent_used"]
        sources = mock["sources"]
        
    elapsed = int((time.time() - start) * 1000)

    return ChatResponse(
        answer=answer,
        intent=intent,
        agent_used=agent_used,
        sources=sources,
        conversation_id=request.conversation_id or f"conv_{int(time.time())}",
        response_time_ms=max(elapsed, 120),
    )
