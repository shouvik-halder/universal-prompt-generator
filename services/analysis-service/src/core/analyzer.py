import time
import uuid

from ..models import (
    AnalysisRequest,
    AnalysisResponse,
)
from .intent.classifier import classify_intent
from .entity.extractor import extract_entities
from .placeholder.detector import detect_placeholders
from .assumption.generator import generate_assumptions


def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """
    Main analysis function that orchestrates all NLU components.
    
    Pipeline:
    1. Classify intent
    2. Extract entities
    3. Detect missing placeholders
    4. Generate assumptions
    """
    start_time = time.time()
    request_id = f"analysis_{uuid.uuid4().hex[:12]}"
    
    # Step 1: Intent classification
    intent = classify_intent(request.text, request.context)
    
    # Step 2: Entity extraction
    entities = extract_entities(request.text, intent.primary, request.context)
    
    # Step 3: Placeholder detection
    placeholders = detect_placeholders(request.text, intent.primary, entities)
    
    # Step 4: Assumption generation
    assumptions = generate_assumptions(request.text, intent.primary, entities, request.context)
    
    # Calculate processing time
    processing_time = (time.time() - start_time) * 1000
    
    return AnalysisResponse(
        request_id=request_id,
        original_text=request.text,
        intent=intent,
        entities=entities,
        placeholders=placeholders,
        assumptions=assumptions,
        processing_time_ms=round(processing_time, 2)
    )