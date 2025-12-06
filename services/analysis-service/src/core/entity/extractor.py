import re
from src.models import IntentType, EntityType, Entity


# Entity extraction patterns per intent
ENTITY_PATTERNS: dict[IntentType, list[tuple[EntityType, str, str]]] = {
    IntentType.EMAIL_WRITING: [
        (EntityType.RECIPIENT, r"\b(?:to|for)\s+(?:my\s+)?(\w+(?:\s+\w+)?)", "recipient"),
        (EntityType.RECIPIENT, r"\b(?:dear)\s+(\w+)", "recipient"),
        (EntityType.SUBJECT, r"\b(?:about|regarding|re:?)\s+(.+?)(?:\.|,|$)", "subject"),
        (EntityType.TONE, r"\b(professional|formal|casual|friendly|urgent|polite)\b", "tone"),
    ],
    IntentType.CODE_GENERATION: [
        (EntityType.PROGRAMMING_LANGUAGE, r"\b(python|javascript|typescript|java|rust|go|golang|c\+\+|cpp|ruby|php|swift|kotlin|scala|r)\b", "language"),
        (EntityType.FRAMEWORK, r"\b(react|vue|angular|django|flask|fastapi|express|nextjs|spring|rails|laravel)\b", "framework"),
        (EntityType.TOPIC, r"\b(?:function|class|method|api|script)\s+(?:to|that|for)\s+(.+?)(?:\.|,|$)", "purpose"),
    ],
    IntentType.IMAGE_GENERATION: [
        (EntityType.SUBJECT, r"\b(?:image|picture|photo|illustration)\s+(?:of|showing|with)\s+(.+?)(?:\.|,|in\s+|$)", "subject"),
        (EntityType.STYLE, r"\b(realistic|photorealistic|abstract|cartoon|anime|oil painting|watercolor|digital art|3d render|cinematic)\b", "style"),
        (EntityType.TONE, r"\b(dark|bright|moody|vibrant|muted|warm|cool|dramatic)\b", "mood"),
    ],
    IntentType.TRANSLATION: [
        (EntityType.LANGUAGE, r"\b(?:from)\s+(english|spanish|french|german|chinese|japanese|korean|arabic|russian|portuguese|italian|hindi)\b", "source_language"),
        (EntityType.LANGUAGE, r"\b(?:to|into)\s+(english|spanish|french|german|chinese|japanese|korean|arabic|russian|portuguese|italian|hindi)\b", "target_language"),
    ],
    IntentType.CREATIVE_WRITING: [
        (EntityType.STYLE, r"\b(fantasy|sci-fi|romance|thriller|horror|mystery|comedy|drama|adventure)\b", "genre"),
        (EntityType.LENGTH, r"\b(short story|flash fiction|novel|novella|paragraph|page|words?)\b", "length"),
        (EntityType.TOPIC, r"\b(?:about|featuring|with)\s+(.+?)(?:\.|,|$)", "topic"),
    ],
    IntentType.SUMMARIZATION: [
        (EntityType.LENGTH, r"\b(\d+)\s*(?:words?|sentences?|paragraphs?|bullet points?)\b", "length"),
        (EntityType.FORMAT, r"\b(bullet points?|numbered list|paragraph|brief|detailed)\b", "format"),
    ],
}

# General patterns that apply to all intents
GENERAL_PATTERNS: list[tuple[EntityType, str, str]] = [
    (EntityType.TONE, r"\b(professional|formal|casual|friendly|serious|humorous|technical|simple)\b", "tone"),
    (EntityType.AUDIENCE, r"\b(?:for)\s+(beginners?|experts?|developers?|managers?|executives?|students?|children|adults)\b", "audience"),
    (EntityType.LENGTH, r"\b(short|long|brief|detailed|concise|comprehensive)\b", "length"),
]


def extract_entities(text: str, intent: IntentType, context: str | None = None) -> list[Entity]:
    """Extract entities from text based on the detected intent."""
    
    full_text = text
    if context:
        full_text = f"{full_text} {context}"
    
    entities: list[Entity] = []
    seen_values: set[str] = set()
    
    # Get intent-specific patterns
    intent_patterns = ENTITY_PATTERNS.get(intent, [])
    
    # Apply intent-specific patterns
    for entity_type, pattern, name in intent_patterns:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            value = match.group(1) if match.groups() else match.group(0)
            value = value.strip().lower()
            
            if value and value not in seen_values:
                seen_values.add(value)
                entities.append(Entity(
                    type=entity_type,
                    value=value,
                    confidence=0.85,
                    start=match.start(),
                    end=match.end()
                ))
    
    # Apply general patterns
    for entity_type, pattern, name in GENERAL_PATTERNS:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            value = match.group(1) if match.groups() else match.group(0)
            value = value.strip().lower()
            
            if value and value not in seen_values:
                seen_values.add(value)
                entities.append(Entity(
                    type=entity_type,
                    value=value,
                    confidence=0.75,
                    start=match.start(),
                    end=match.end()
                ))
    
    return entities