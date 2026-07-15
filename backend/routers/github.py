from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from agents.github_agent import search_mistral_repos

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

@router.get("/repos", response_model=List[GitHubRepo])
async def get_repos():
    raw_repos = search_mistral_repos()
    repos = []
    for r in raw_repos:
        repos.append(GitHubRepo(
            id=r["id"],
            name=r["name"],
            full_name=r.get("full_name", f"mistralai/{r['name']}"),
            description=r.get("description", ""),
            url=r.get("url", ""),
            stars=r.get("stars", 0),
            forks=r.get("forks", 0),
            language=r.get("language", "Unknown"),
            topics=r.get("topics", []),
            last_updated=r.get("last_updated", ""),
            open_issues=r.get("open_issues", 0),
            license=r.get("license", "Unknown")
        ))
    return repos

@router.get("/repos/{repo_id}", response_model=GitHubRepo)
async def get_repo(repo_id: str):
    repos = await get_repos()
    for repo in repos:
        if repo.id == repo_id or repo.name == repo_id:
            return repo
    raise HTTPException(status_code=404, detail=f"Repo '{repo_id}' not found")
