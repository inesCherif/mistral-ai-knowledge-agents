"""GitHub router — Phase 1: Static repo data, Phase 4: GitHub API live"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class GitHubRepo(BaseModel):
    id: str
    name: str
    full_name: str
    description: str
    url: str
    stars: int
    forks: int
    language: str
    topics: List[str]
    last_updated: str
    open_issues: int
    license: str


REPOS_DATA: List[GitHubRepo] = [
    GitHubRepo(
        id="mistral-src",
        name="mistral-src",
        full_name="mistralai/mistral-src",
        description="Reference implementation of Mistral AI's models. Includes the model architecture and inference code.",
        url="https://github.com/mistralai/mistral-src",
        stars=9200,
        forks=890,
        language="Python",
        topics=["llm", "mistral", "transformer", "inference"],
        last_updated="2024-06-15",
        open_issues=42,
        license="Apache 2.0",
    ),
    GitHubRepo(
        id="mistral-inference",
        name="mistral-inference",
        full_name="mistralai/mistral-inference",
        description="Official inference library for Mistral models. Optimized for performance with FlashAttention2 support.",
        url="https://github.com/mistralai/mistral-inference",
        stars=7400,
        forks=620,
        language="Python",
        topics=["inference", "llm", "mistral", "flashattention"],
        last_updated="2024-07-01",
        open_issues=28,
        license="Apache 2.0",
    ),
    GitHubRepo(
        id="mistral-finetune",
        name="mistral-finetune",
        full_name="mistralai/mistral-finetune",
        description="A lightweight codebase to fine-tune Mistral models. Supports LoRA and full fine-tuning.",
        url="https://github.com/mistralai/mistral-finetune",
        stars=3100,
        forks=280,
        language="Python",
        topics=["fine-tuning", "lora", "llm", "mistral"],
        last_updated="2024-06-28",
        open_issues=15,
        license="Apache 2.0",
    ),
    GitHubRepo(
        id="client-python",
        name="client-python",
        full_name="mistralai/client-python",
        description="Official Python client for the Mistral AI API. Supports async, streaming, and function calling.",
        url="https://github.com/mistralai/client-python",
        stars=1800,
        forks=190,
        language="Python",
        topics=["api-client", "mistral", "python", "sdk"],
        last_updated="2024-07-05",
        open_issues=12,
        license="Apache 2.0",
    ),
    GitHubRepo(
        id="client-js",
        name="client-js",
        full_name="mistralai/client-js",
        description="Official JavaScript/TypeScript client for the Mistral AI API. Supports Node.js and browser environments.",
        url="https://github.com/mistralai/client-js",
        stars=920,
        forks=95,
        language="TypeScript",
        topics=["api-client", "mistral", "typescript", "sdk"],
        last_updated="2024-07-03",
        open_issues=8,
        license="Apache 2.0",
    ),
]


@router.get("/repos", response_model=List[GitHubRepo])
async def get_repos():
    return REPOS_DATA


@router.get("/repos/{repo_id}", response_model=GitHubRepo)
async def get_repo(repo_id: str):
    for repo in REPOS_DATA:
        if repo.id == repo_id:
            return repo
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Repo '{repo_id}' not found")
