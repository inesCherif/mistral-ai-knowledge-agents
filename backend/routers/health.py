from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "mistralbot-api",
        "version": "0.1.0",
        "agents": {
            "site_agent": "ready",
            "models_agent": "ready",
            "research_agent": "ready",
            "github_agent": "ready",
            "contact_agent": "ready",
        },
    }
