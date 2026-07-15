"""Models router — Phase 1: Static data, Phase 2: RAG-powered"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class MistralModel(BaseModel):
    id: str
    name: str
    description: str
    parameters: str
    context_length: int
    license: str
    type: str  # "generalist" | "code" | "math" | "embed" | "moe"
    api_endpoint: Optional[str] = None
    open_source: bool
    release_date: str
    benchmarks: dict = {}


MODELS_DATA: List[MistralModel] = [
    MistralModel(
        id="mistral-7b",
        name="Mistral 7B",
        description="The original Mistral model. Outperforms Llama 2 13B on most benchmarks despite being half the size. Uses Grouped Query Attention (GQA) and Sliding Window Attention (SWA).",
        parameters="7.3B",
        context_length=32768,
        license="Apache 2.0",
        type="generalist",
        open_source=True,
        release_date="2023-09-27",
        benchmarks={"MMLU": 60.1, "HumanEval": 30.5, "GSM8K": 52.2, "HellaSwag": 81.3},
    ),
    MistralModel(
        id="mixtral-8x7b",
        name="Mixtral 8x7B",
        description="Sparse Mixture of Experts (MoE) model. 8 experts of 7B each, 2 active per token. Matches GPT-3.5 performance with less compute.",
        parameters="45B total / 12.9B active",
        context_length=32768,
        license="Apache 2.0",
        type="moe",
        open_source=True,
        release_date="2023-12-11",
        benchmarks={"MMLU": 70.6, "HumanEval": 40.2, "GSM8K": 74.4, "HellaSwag": 86.7},
    ),
    MistralModel(
        id="mistral-large",
        name="Mistral Large",
        description="Top-tier model for complex reasoning tasks. Supports 80+ languages. Best model for tasks requiring advanced reasoning.",
        parameters="~123B",
        context_length=131072,
        license="Mistral Research License",
        type="generalist",
        api_endpoint="mistral-large-latest",
        open_source=False,
        release_date="2024-02-26",
        benchmarks={"MMLU": 81.2, "HumanEval": 45.1, "GSM8K": 81.0},
    ),
    MistralModel(
        id="codestral",
        name="Codestral",
        description="Specialized code generation model. Supports 80+ programming languages. Optimized for fill-in-the-middle (FIM) completions.",
        parameters="22B",
        context_length=32768,
        license="Mistral Non-Production License",
        type="code",
        api_endpoint="codestral-latest",
        open_source=False,
        release_date="2024-05-29",
        benchmarks={"HumanEval": 81.1, "RepoBench": 78.2},
    ),
    MistralModel(
        id="mathstral",
        name="Mathstral",
        description="Mathematical reasoning model fine-tuned for STEM tasks. Based on Mistral 7B, specialized for solving complex math problems.",
        parameters="7B",
        context_length=32768,
        license="Apache 2.0",
        type="math",
        open_source=True,
        release_date="2024-07-16",
        benchmarks={"MATH": 56.6, "GSM8K": 78.9},
    ),
    MistralModel(
        id="mistral-embed",
        name="Mistral Embed",
        description="Embedding model for semantic search and RAG applications. Produces 1024-dimensional vectors.",
        parameters="~1B",
        context_length=8192,
        license="Mistral Terms",
        type="embed",
        api_endpoint="mistral-embed",
        open_source=False,
        release_date="2023-12-11",
        benchmarks={"MTEB": 64.8},
    ),
]


@router.get("/", response_model=List[MistralModel])
async def get_models():
    return MODELS_DATA


@router.get("/{model_id}", response_model=MistralModel)
async def get_model(model_id: str):
    for model in MODELS_DATA:
        if model.id == model_id:
            return model
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")
