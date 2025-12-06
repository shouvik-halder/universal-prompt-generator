from typing import Optional, Any
from pydantic import BaseModel


class IntentData(BaseModel):
    primary: str
    confidence: float
    secondary: list[tuple[str, float]] = []


class EntityData(BaseModel):
    type: str
    value: str
    confidence: float


class PlaceholderData(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[str] = None


class AssumptionData(BaseModel):
    category: str
    value: str
    confidence: float
    reasoning: str


class AnalysisData(BaseModel):
    """Analysis data received from analysis-service."""
    request_id: str
    original_text: str
    intent: IntentData
    entities: list[EntityData]
    placeholders: list[PlaceholderData]
    assumptions: list[AssumptionData]


class GenerationRequest(BaseModel):
    """Request to generate prompts."""
    analysis: AnalysisData
    platforms: Optional[list[str]] = None  # If None, generate for all applicable
    options: Optional[dict] = None


class GeneratedPrompt(BaseModel):
    """A single generated prompt for a platform."""
    platform: str
    platform_name: str
    prompt: str
    placeholders: list[dict]
    settings: dict


class GenerationResponse(BaseModel):
    """Response containing all generated prompts."""
    request_id: str
    intent: str
    prompts: dict[str, GeneratedPrompt]
    assumptions: list[dict]
    processing_time_ms: float


class PlatformResponse(BaseModel):
    id: str
    name: str
    type: str
    enabled: bool


class IntentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    enabled: bool