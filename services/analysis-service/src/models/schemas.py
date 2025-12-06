from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class IntentType(str, Enum):
    EMAIL_WRITING = "email_writing"
    CODE_GENERATION = "code_generation"
    IMAGE_GENERATION = "image_generation"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    CREATIVE_WRITING = "creative_writing"
    QUESTION_ANSWERING = "question_answering"
    ANALYSIS = "analysis"
    GENERAL = "general"


class EntityType(str, Enum):
    RECIPIENT = "recipient"
    SUBJECT = "subject"
    TONE = "tone"
    LANGUAGE = "language"
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    STYLE = "style"
    FORMAT = "format"
    LENGTH = "length"
    AUDIENCE = "audience"
    TOPIC = "topic"
    CUSTOM = "custom"


class AssumptionCategory(str, Enum):
    TONE = "tone"
    AUDIENCE = "audience"
    FORMAT = "format"
    CONTEXT = "context"
    STYLE = "style"
    LENGTH = "length"


class Intent(BaseModel):
    primary: IntentType
    confidence: float = Field(ge=0.0, le=1.0)
    secondary: list[tuple[IntentType, float]] = []


class Entity(BaseModel):
    type: EntityType
    value: str
    confidence: float = Field(ge=0.0, le=1.0)
    start: Optional[int] = None
    end: Optional[int] = None


class Placeholder(BaseModel):
    name: str
    type: EntityType
    description: str
    required: bool = True
    default: Optional[str] = None


class Assumption(BaseModel):
    category: AssumptionCategory
    value: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    context: Optional[str] = None


class AnalysisResponse(BaseModel):
    request_id: str
    original_text: str
    intent: Intent
    entities: list[Entity]
    placeholders: list[Placeholder]
    assumptions: list[Assumption]
    processing_time_ms: float