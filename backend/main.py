"""
MistralBot Backend — FastAPI Application Entry Point
Phase 1: Skeleton with mock responses
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import chat, health, models, research, github, contacts

app = FastAPI(
    title="MistralBot API",
    description="Agentic RAG chatbot about Mistral AI",
    version="0.1.0",
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(github.router, prefix="/api/github", tags=["github"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["contacts"])


@app.get("/")
async def root():
    return {
        "name": "MistralBot API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }
