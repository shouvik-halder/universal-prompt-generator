from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import (
    GenerationRequest,
    GenerationResponse,
    PlatformResponse,
    IntentResponse,
)
from ..core import generate_prompts, AdapterRegistry
from ..db import get_session, Platform, Intent

router = APIRouter()


@router.post("/generate", response_model=GenerationResponse)
async def generate(
    request: GenerationRequest,
    session: AsyncSession = Depends(get_session)
) -> GenerationResponse:
    """
    Generate optimized prompts for multiple AI platforms.
    
    Accepts analysis data and returns platform-specific prompts.
    """
    try:
        result = await generate_prompts(request, session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platforms", response_model=list[PlatformResponse])
async def list_platforms(
    session: AsyncSession = Depends(get_session)
) -> list[PlatformResponse]:
    """List all available platforms."""
    try:
        # Try database first
        result = await session.execute(select(Platform).where(Platform.enabled == True))
        platforms = result.scalars().all()
        
        if platforms:
            return [
                PlatformResponse(
                    id=p.id,
                    name=p.name,
                    type=p.type,
                    enabled=p.enabled
                )
                for p in platforms
            ]
    except:
        pass
    
    # Fall back to adapters
    adapters = AdapterRegistry.get_all()
    return [
        PlatformResponse(
            id=a.platform_id,
            name=a.platform_name,
            type=a.platform_type,
            enabled=True
        )
        for a in adapters
    ]


@router.get("/intents", response_model=list[IntentResponse])
async def list_intents(
    session: AsyncSession = Depends(get_session)
) -> list[IntentResponse]:
    """List all available intents."""
    try:
        result = await session.execute(select(Intent).where(Intent.enabled == True))
        intents = result.scalars().all()
        
        if intents:
            return [
                IntentResponse(
                    id=i.id,
                    name=i.name,
                    description=i.description,
                    enabled=i.enabled
                )
                for i in intents
            ]
    except:
        pass
    
    # Fall back to hardcoded list
    return [
        IntentResponse(id="email_writing", name="Email Writing", description="Professional and personal emails", enabled=True),
        IntentResponse(id="code_generation", name="Code Generation", description="Code, scripts, and functions", enabled=True),
        IntentResponse(id="image_generation", name="Image Generation", description="AI image prompts", enabled=True),
        IntentResponse(id="summarization", name="Summarization", description="Content summarization", enabled=True),
        IntentResponse(id="translation", name="Translation", description="Language translation", enabled=True),
        IntentResponse(id="creative_writing", name="Creative Writing", description="Stories and creative content", enabled=True),
    ]


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "generation-service"}


@router.get("/ready")
async def ready():
    """Readiness check endpoint."""
    return {"ready": True}