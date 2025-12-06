import re
from src.models import IntentType, Intent


# Intent patterns: (regex, weight)
INTENT_PATTERNS: dict[IntentType, list[tuple[str, float]]] = {
    IntentType.EMAIL_WRITING: [
        (r"\b(email|e-mail|mail|message)\b", 0.4),
        (r"\b(send|compose|write|draft)\b.*\b(to|for)\b", 0.3),
        (r"\b(subject|recipient|dear|regards|sincerely)\b", 0.2),
        (r"\b(boss|manager|client|colleague|team)\b", 0.15),
        (r"\b(professional|formal|business)\b", 0.1),
    ],
    IntentType.CODE_GENERATION: [
        (r"\b(code|program|script|function|class|method)\b", 0.35),
        (r"\b(python|javascript|typescript|java|rust|go|c\+\+|ruby|php)\b", 0.35),
        (r"\b(implement|create|build|develop|write)\b.*\b(function|class|api|app)\b", 0.25),
        (r"\b(algorithm|data structure|api|endpoint|database)\b", 0.2),
        (r"\b(debug|fix|refactor|optimize)\b", 0.15),
    ],
    IntentType.IMAGE_GENERATION: [
        (r"\b(image|picture|photo|illustration|artwork|drawing)\b", 0.4),
        (r"\b(generate|create|make|draw|paint|render)\b.*\b(image|picture|visual)\b", 0.35),
        (r"\b(midjourney|dall-?e|stable diffusion|sdxl)\b", 0.4),
        (r"\b(portrait|landscape|scene|background|character)\b", 0.2),
        (r"\b(style|artistic|realistic|abstract|digital art)\b", 0.15),
    ],
    IntentType.SUMMARIZATION: [
        (r"\b(summarize|summary|summarise|condense|shorten)\b", 0.5),
        (r"\b(brief|overview|key points|main points|tldr|tl;dr)\b", 0.3),
        (r"\b(digest|recap|synopsis)\b", 0.25),
    ],
    IntentType.TRANSLATION: [
        (r"\b(translate|translation|convert)\b", 0.5),
        (r"\b(from|to)\b\s*(english|spanish|french|german|chinese|japanese|korean|arabic|russian|portuguese|italian|hindi)\b", 0.35),
        (r"\b(in|into)\b\s*(english|spanish|french|german|chinese|japanese|korean|arabic|russian|portuguese|italian|hindi)\b", 0.35),
        (r"\b(language|localize|localization)\b", 0.2),
    ],
    IntentType.CREATIVE_WRITING: [
        (r"\b(story|narrative|tale|fiction|novel)\b", 0.4),
        (r"\b(poem|poetry|verse|haiku|sonnet)\b", 0.35),
        (r"\b(creative|imaginative|fantasy|sci-fi|romance|thriller|horror)\b", 0.25),
        (r"\b(character|plot|setting|dialogue)\b", 0.2),
        (r"\b(write|compose|create)\b.*\b(story|poem|narrative)\b", 0.3),
    ],
    IntentType.QUESTION_ANSWERING: [
        (r"^(what|who|where|when|why|how|which|can|could|would|should|is|are|do|does)\b", 0.35),
        (r"\?\s*$", 0.3),
        (r"\b(explain|tell me|describe|define)\b", 0.25),
        (r"\b(what is|what are|how to|how do)\b", 0.3),
    ],
    IntentType.ANALYSIS: [
        (r"\b(analyze|analyse|analysis|evaluate|assess)\b", 0.45),
        (r"\b(compare|contrast|pros and cons|advantages|disadvantages)\b", 0.3),
        (r"\b(review|examine|investigate|study)\b", 0.25),
        (r"\b(strengths|weaknesses|opportunities|threats)\b", 0.2),
    ],
}


def classify_intent(text: str, context: str | None = None) -> Intent:
    """Classify the intent of the input text using pattern matching."""
    
    full_text = text.lower()
    if context:
        full_text = f"{full_text} {context.lower()}"
    
    scores: dict[IntentType, float] = {}
    
    for intent_type, patterns in INTENT_PATTERNS.items():
        score = 0.0
        matches = 0
        
        for pattern, weight in patterns:
            if re.search(pattern, full_text, re.IGNORECASE):
                score += weight
                matches += 1
        
        if matches > 0:
            # Normalize and add match bonus
            normalized = score / len(patterns)
            match_bonus = min(matches * 0.05, 0.2)
            scores[intent_type] = min(normalized + match_bonus, 1.0)
    
    # Sort by score
    sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    if sorted_intents and sorted_intents[0][1] >= 0.1:
        primary = sorted_intents[0][0]
        confidence = round(sorted_intents[0][1], 3)
    else:
        primary = IntentType.GENERAL
        confidence = 0.5
    
    # Get secondary intents
    secondary = [
        (intent, round(score, 3))
        for intent, score in sorted_intents[1:4]
        if score >= 0.15
    ]
    
    return Intent(primary=primary, confidence=confidence, secondary=secondary)