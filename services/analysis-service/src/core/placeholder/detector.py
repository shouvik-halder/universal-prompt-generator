from src.models import IntentType, EntityType, Entity, Placeholder


# Required placeholders per intent (if not found in entities)
INTENT_PLACEHOLDERS: dict[IntentType, list[dict]] = {
    IntentType.EMAIL_WRITING: [
        {"name": "RECIPIENT_NAME", "type": EntityType.RECIPIENT, "description": "Name of the email recipient", "required": True},
        {"name": "RECIPIENT_ROLE", "type": EntityType.RECIPIENT, "description": "Role/position of recipient (e.g., manager, client)", "required": False},
        {"name": "EMAIL_SUBJECT", "type": EntityType.SUBJECT, "description": "Main subject/purpose of the email", "required": True},
        {"name": "SENDER_NAME", "type": EntityType.CUSTOM, "description": "Your name for the signature", "required": False, "default": "[Your Name]"},
        {"name": "TONE", "type": EntityType.TONE, "description": "Desired tone (professional, friendly, formal)", "required": False, "default": "professional"},
    ],
    IntentType.CODE_GENERATION: [
        {"name": "LANGUAGE", "type": EntityType.PROGRAMMING_LANGUAGE, "description": "Programming language to use", "required": True},
        {"name": "TASK_DESCRIPTION", "type": EntityType.TOPIC, "description": "What the code should accomplish", "required": True},
        {"name": "FRAMEWORK", "type": EntityType.FRAMEWORK, "description": "Framework to use (if applicable)", "required": False},
    ],
    IntentType.IMAGE_GENERATION: [
        {"name": "SUBJECT", "type": EntityType.SUBJECT, "description": "Main subject of the image", "required": True},
        {"name": "STYLE", "type": EntityType.STYLE, "description": "Artistic style (realistic, cartoon, etc.)", "required": False, "default": "realistic"},
        {"name": "MOOD", "type": EntityType.TONE, "description": "Mood/atmosphere of the image", "required": False},
        {"name": "ASPECT_RATIO", "type": EntityType.FORMAT, "description": "Image aspect ratio (16:9, 1:1, etc.)", "required": False, "default": "16:9"},
    ],
    IntentType.TRANSLATION: [
        {"name": "SOURCE_LANGUAGE", "type": EntityType.LANGUAGE, "description": "Language to translate from", "required": True},
        {"name": "TARGET_LANGUAGE", "type": EntityType.LANGUAGE, "description": "Language to translate to", "required": True},
        {"name": "TEXT_TO_TRANSLATE", "type": EntityType.CUSTOM, "description": "The text that needs translation", "required": True},
    ],
    IntentType.SUMMARIZATION: [
        {"name": "CONTENT", "type": EntityType.CUSTOM, "description": "The content to summarize", "required": True},
        {"name": "LENGTH", "type": EntityType.LENGTH, "description": "Desired summary length", "required": False, "default": "concise"},
        {"name": "FORMAT", "type": EntityType.FORMAT, "description": "Output format (paragraph, bullet points)", "required": False, "default": "paragraph"},
    ],
    IntentType.CREATIVE_WRITING: [
        {"name": "GENRE", "type": EntityType.STYLE, "description": "Genre of the writing", "required": False, "default": "general fiction"},
        {"name": "TOPIC", "type": EntityType.TOPIC, "description": "Main topic or premise", "required": True},
        {"name": "LENGTH", "type": EntityType.LENGTH, "description": "Desired length", "required": False, "default": "short story"},
        {"name": "TONE", "type": EntityType.TONE, "description": "Tone/mood of the writing", "required": False},
    ],
    IntentType.QUESTION_ANSWERING: [
        {"name": "QUESTION", "type": EntityType.CUSTOM, "description": "The question to answer", "required": True},
        {"name": "CONTEXT", "type": EntityType.CUSTOM, "description": "Additional context if needed", "required": False},
    ],
    IntentType.ANALYSIS: [
        {"name": "SUBJECT", "type": EntityType.TOPIC, "description": "What to analyze", "required": True},
        {"name": "CRITERIA", "type": EntityType.CUSTOM, "description": "Criteria or aspects to focus on", "required": False},
        {"name": "FORMAT", "type": EntityType.FORMAT, "description": "Output format", "required": False, "default": "structured analysis"},
    ],
    IntentType.GENERAL: [
        {"name": "TASK", "type": EntityType.CUSTOM, "description": "What you want to accomplish", "required": True},
        {"name": "DETAILS", "type": EntityType.CUSTOM, "description": "Additional details or requirements", "required": False},
    ],
}


def detect_placeholders(
    text: str,
    intent: IntentType,
    entities: list[Entity]
) -> list[Placeholder]:
    """Detect missing information that should be filled as placeholders."""
    
    placeholders: list[Placeholder] = []
    entity_types_found = {e.type for e in entities}
    entity_values = {e.value.lower() for e in entities}
    
    # Get required placeholders for this intent
    intent_placeholders = INTENT_PLACEHOLDERS.get(intent, INTENT_PLACEHOLDERS[IntentType.GENERAL])
    
    for ph_def in intent_placeholders:
        ph_type = ph_def["type"]
        
        # Check if this type of entity was already extracted
        if ph_type in entity_types_found:
            continue
        
        # Create placeholder
        placeholder = Placeholder(
            name=ph_def["name"],
            type=ph_type,
            description=ph_def["description"],
            required=ph_def.get("required", True),
            default=ph_def.get("default")
        )
        placeholders.append(placeholder)
    
    return placeholders