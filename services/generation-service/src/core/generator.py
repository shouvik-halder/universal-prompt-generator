import time
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import (
    AnalysisData,
    GenerationRequest,
    GenerationResponse,
    GeneratedPrompt,
)
from src.core.adapters import AdapterRegistry
from src.core.template import TemplateLoader


async def generate_prompts(
    request: GenerationRequest,
    session: Optional[AsyncSession] = None
) -> GenerationResponse:
    """
    Generate prompts for all requested platforms.
    
    Args:
        request: Generation request with analysis data
        session: Optional database session for template lookup
    
    Returns:
        GenerationResponse with prompts for each platform
    """
    start_time = time.time()
    request_id = f"gen_{uuid.uuid4().hex[:12]}"
    
    analysis = request.analysis
    intent = analysis.intent.primary
    
    # Initialize template loader
    loader = TemplateLoader(session)
    
    # Determine which platforms to generate for
    if request.platforms:
        # Use specified platforms
        platform_ids = request.platforms
    else:
        # Get all platforms that support this intent
        adapters = AdapterRegistry.get_for_intent(intent)
        platform_ids = [a.platform_id for a in adapters]
    
    # Generate for each platform
    prompts: dict[str, GeneratedPrompt] = {}
    
    for platform_id in platform_ids:
        adapter = AdapterRegistry.get(platform_id)
        if not adapter:
            continue
        
        if not adapter.supports_intent(intent):
            continue
        
        # Get template
        template_content = await loader.get_template(platform_id, intent)
        if not template_content:
            # Use default template
            template_content = loader.get_default_template(platform_id, intent)
        
        # Generate prompt
        try:
            generated = adapter.generate(analysis, template_content)
            prompts[platform_id] = generated
        except Exception as e:
            # Log error but continue with other platforms
            print(f"Error generating for {platform_id}: {e}")
            continue
    
    # Calculate processing time
    processing_time = (time.time() - start_time) * 1000
    
    # Build assumptions list
    assumptions = [
        {
            "category": a.category,
            "value": a.value,
            "confidence": a.confidence,
            "reasoning": a.reasoning,
        }
        for a in analysis.assumptions
    ]
    
    return GenerationResponse(
        request_id=request_id,
        intent=intent,
        prompts=prompts,
        assumptions=assumptions,
        processing_time_ms=round(processing_time, 2)
    )