from fastapi import APIRouter, HTTPException

from src.models import AnalysisRequest, AnalysisResponse
from src.core.analyzer import analyze

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze input text and return structured NLU results.
    
    Returns:
    - Intent classification (primary + secondary)
    - Extracted entities
    - Missing placeholders
    - Generated assumptions
    """
    try:
        result = analyze(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "analysis-service"}


@router.get("/ready")
async def ready():
    """Readiness check endpoint."""
    return {"ready": True}