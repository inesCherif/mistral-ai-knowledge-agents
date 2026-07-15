"""Research router — Phase 1: Static papers data, Phase 3: arXiv live search"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class Paper(BaseModel):
    id: str
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    published: str
    url: str
    pdf_url: str
    categories: List[str]
    benchmarks: Optional[dict] = {}


PAPERS_DATA: List[Paper] = [
    Paper(
        id="mistral-7b",
        arxiv_id="2310.06825",
        title="Mistral 7B",
        authors=["Albert Q. Jiang", "Alexandre Sablayrolles", "Arthur Mensch",
                 "Chris Bamford", "Devendra Singh Chaplot", "Diego de las Casas",
                 "Florian Bressand", "Gianna Lengyel", "Guillaume Lample",
                 "Lucile Saulnier", "Lélio Renard Lavaud", "Marie-Anne Lachaux",
                 "Pierre Stock", "Teven Le Scao", "Thibaut Lavril",
                 "Thomas Wang", "Timothée Lacroix", "William El Sayed"],
        abstract=(
            "We introduce Mistral 7B, a 7-billion-parameter language model engineered for "
            "superior performance and efficiency. Mistral 7B outperforms the best open 13B "
            "model (Llama 2) across all evaluated benchmarks, and the best released 34B model "
            "(Llama 1) in reasoning, mathematics and code generation. Our model leverages "
            "grouped-query attention (GQA) for faster inference, coupled with sliding window "
            "attention (SWA) to effectively handle sequences of arbitrary length with a reduced "
            "inference cost. We also provide a model fine-tuned to follow instructions, "
            "Mistral 7B – Instruct, that surpasses Llama 2 13B – chat model both on human "
            "and automated benchmarks."
        ),
        published="2023-10-10",
        url="https://arxiv.org/abs/2310.06825",
        pdf_url="https://arxiv.org/pdf/2310.06825",
        categories=["cs.CL", "cs.LG"],
        benchmarks={"MMLU": 60.1, "HumanEval": 30.5, "GSM8K": 52.2, "HellaSwag": 81.3, "WinoGrande": 75.3},
    ),
    Paper(
        id="mixtral-8x7b",
        arxiv_id="2401.04088",
        title="Mixtral of Experts",
        authors=["Albert Q. Jiang", "Alexandre Sablayrolles", "Antoine Roux",
                 "Arthur Mensch", "Blanche Savary", "Chris Bamford",
                 "Devendra Singh Chaplot", "Diego de las Casas", "Emma Bou Hanna",
                 "Florian Bressand", "Gianna Lengyel", "Guillaume Bour",
                 "Guillaume Lample", "Lélio Renard Lavaud", "Lucile Saulnier",
                 "Marie-Anne Lachaux", "Pierre Stock", "Sandeep Subramanian",
                 "Sophia Yang", "Szymon Antoniak", "Teven Le Scao",
                 "Théophile Gervet", "Thibaut Lavril", "Thomas Wang",
                 "Timothée Lacroix", "William El Sayed"],
        abstract=(
            "We introduce Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language model. "
            "Mixtral has the same architecture as Mistral 7B, with the difference that each "
            "layer is composed of 8 feedforward blocks (i.e. experts). For every token, at "
            "each layer, a router network selects two experts to process the current state and "
            "combine their outputs. Even though each token only sees two experts, the selected "
            "experts can be different at each timestep."
        ),
        published="2024-01-08",
        url="https://arxiv.org/abs/2401.04088",
        pdf_url="https://arxiv.org/pdf/2401.04088",
        categories=["cs.LG", "cs.CL"],
        benchmarks={"MMLU": 70.6, "HumanEval": 40.2, "GSM8K": 74.4, "HellaSwag": 86.7, "WinoGrande": 81.2},
    ),
]


@router.get("/papers", response_model=List[Paper])
async def get_papers():
    return PAPERS_DATA


@router.get("/papers/{paper_id}", response_model=Paper)
async def get_paper(paper_id: str):
    for paper in PAPERS_DATA:
        if paper.id == paper_id:
            return paper
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Paper '{paper_id}' not found")
