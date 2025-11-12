from fastapi import APIRouter, HTTPException
from typing import List
from schemas import GenerateRequest, GenerateResponse
from llm_service import LLMService

router = APIRouter(prefix="/api/llm", tags=["LLM"])
llm_service = LLMService()

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    result = await llm_service.generate(
        prompt=request.prompt,
        provider=request.provider,
        model=request.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Generation failed"))
    
    return GenerateResponse(**result)

@router.get("/providers")
async def get_providers() -> List[str]:
    return llm_service.get_available_providers()

@router.get("/health")
async def health_check():
    providers = llm_service.get_available_providers()
    return {
        "status": "healthy",
        "available_providers": providers,
        "total_providers": len(providers)
    }
