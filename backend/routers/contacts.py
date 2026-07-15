"""Contacts router — Phase 1: Static data, Phase 5: Web-enriched"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class ContactPerson(BaseModel):
    id: str
    name: str
    role: str
    department: str
    location: str
    bio: str
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    github: Optional[str] = None
    email: Optional[str] = None  # Only public emails
    arxiv_author: Optional[str] = None
    avatar_initials: str
    avatar_color: str


class OfficialContact(BaseModel):
    type: str
    label: str
    value: str
    url: Optional[str] = None


TEAM_DATA: List[ContactPerson] = [
    ContactPerson(
        id="arthur-mensch",
        name="Arthur Mensch",
        role="CEO & Co-founder",
        department="Leadership",
        location="Paris, France",
        bio=(
            "Arthur Mensch co-founded Mistral AI in April 2023. "
            "Previously a research scientist at DeepMind, where he worked on "
            "large-scale machine learning. He holds a PhD from École Polytechnique / Inria."
        ),
        linkedin="https://www.linkedin.com/in/arthur-mensch/",
        twitter="https://twitter.com/arthurmensch",
        github="https://github.com/arthurmensch",
        arxiv_author="Arthur Mensch",
        avatar_initials="AM",
        avatar_color="#FF6B35",
    ),
    ContactPerson(
        id="guillaume-lample",
        name="Guillaume Lample",
        role="Co-founder & Chief Scientist",
        department="Research",
        location="Paris, France",
        bio=(
            "Guillaume Lample co-founded Mistral AI. Previously at Meta AI Research "
            "where he was a key contributor to the LLaMA models and Galactica. "
            "PhD in NLP from Sorbonne University. Known for his work on sequence-to-sequence models."
        ),
        linkedin="https://www.linkedin.com/in/guillaume-lample/",
        twitter="https://twitter.com/guillaumelample",
        github="https://github.com/glample",
        arxiv_author="Guillaume Lample",
        avatar_initials="GL",
        avatar_color="#4F46E5",
    ),
    ContactPerson(
        id="timothee-lacroix",
        name="Timothée Lacroix",
        role="Co-founder & CTO",
        department="Engineering",
        location="Paris, France",
        bio=(
            "Timothée Lacroix co-founded Mistral AI and leads technical infrastructure. "
            "Previously Staff Engineer at Meta AI Research. He worked on large-scale "
            "distributed training systems and contributed to the LLaMA project."
        ),
        linkedin="https://www.linkedin.com/in/timothee-lacroix/",
        twitter="https://twitter.com/timothee_lacroix",
        arxiv_author="Timothée Lacroix",
        avatar_initials="TL",
        avatar_color="#10B981",
    ),
    ContactPerson(
        id="sophia-yang",
        name="Sophia Yang",
        role="Head of Developer Relations",
        department="Developer Relations",
        location="San Francisco, CA, USA",
        bio=(
            "Sophia Yang leads Developer Relations at Mistral AI. "
            "Previously at Anaconda and Cohere. Active in the open-source AI community, "
            "she creates tutorials and resources for developers using Mistral models."
        ),
        linkedin="https://www.linkedin.com/in/sophiamyang/",
        twitter="https://twitter.com/sophiamyang",
        github="https://github.com/sophiamyang",
        avatar_initials="SY",
        avatar_color="#F59E0B",
    ),
    ContactPerson(
        id="baptiste-roziere",
        name="Baptiste Rozière",
        role="Research Scientist",
        department="Research",
        location="Paris, France",
        bio=(
            "Baptiste Rozière is a Research Scientist at Mistral AI working on code generation. "
            "Previously at Meta AI Research, he created Code Llama. "
            "PhD from Sorbonne University on multilingual code models."
        ),
        linkedin="https://www.linkedin.com/in/baptiste-rozi%C3%A8re/",
        github="https://github.com/baptistr",
        arxiv_author="Baptiste Rozière",
        avatar_initials="BR",
        avatar_color="#8B5CF6",
    ),
]

OFFICIAL_CONTACTS: List[OfficialContact] = [
    OfficialContact(type="email", label="Press & Media", value="press@mistral.ai", url="mailto:press@mistral.ai"),
    OfficialContact(type="email", label="Enterprise Sales", value="enterprise@mistral.ai", url="mailto:enterprise@mistral.ai"),
    OfficialContact(type="email", label="Partnerships", value="partnerships@mistral.ai", url="mailto:partnerships@mistral.ai"),
    OfficialContact(type="social", label="Twitter / X", value="@MistralAI", url="https://twitter.com/MistralAI"),
    OfficialContact(type="social", label="LinkedIn", value="Mistral AI", url="https://www.linkedin.com/company/mistralai/"),
    OfficialContact(type="social", label="Discord", value="discord.gg/mistralai", url="https://discord.gg/mistralai"),
    OfficialContact(type="social", label="GitHub", value="github.com/mistralai", url="https://github.com/mistralai"),
    OfficialContact(type="site", label="Website", value="mistral.ai", url="https://mistral.ai"),
    OfficialContact(type="site", label="API Console", value="console.mistral.ai", url="https://console.mistral.ai"),
]


@router.get("/team", response_model=List[ContactPerson])
async def get_team():
    return TEAM_DATA


@router.get("/team/{person_id}", response_model=ContactPerson)
async def get_person(person_id: str):
    for person in TEAM_DATA:
        if person.id == person_id:
            return person
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found")


@router.get("/official", response_model=List[OfficialContact])
async def get_official_contacts():
    return OFFICIAL_CONTACTS
