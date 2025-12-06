import re
from src.models import IntentType, Entity, AssumptionCategory, Assumption


# Tone detection patterns
TONE_PATTERNS: list[tuple[str, str, float, str]] = [
    (r"\b(boss|manager|supervisor|director|ceo|executive|client)\b", "Professional and formal tone", 0.85, "Detected formal recipient role"),
    (r"\b(professional|formal|business)\b", "Professional and formal tone", 0.9, "Explicit tone indicator"),
    (r"\b(friend|buddy|pal|mate|bro)\b", "Friendly and casual tone", 0.85, "Detected informal recipient"),
    (r"\b(casual|informal|relaxed|friendly)\b", "Casual and conversational tone", 0.9, "Explicit tone indicator"),
    (r"\b(urgent|asap|immediately|critical|emergency)\b", "Direct and urgent tone", 0.8, "Urgency indicators detected"),
]

# Audience detection patterns
AUDIENCE_PATTERNS: list[tuple[str, str, float, str]] = [
    (r"\b(technical|developer|engineer|programmer)\b", "Technical audience with domain expertise", 0.85, "Technical role mentioned"),
    (r"\b(beginner|newbie|novice|learning|new to)\b", "Beginners with limited background", 0.85, "Beginner indicators"),
    (r"\b(expert|advanced|senior|experienced)\b", "Experienced professionals", 0.85, "Expert indicators"),
    (r"\b(executive|leadership|c-suite|board|manager)\b", "Business leadership", 0.8, "Leadership role mentioned"),
    (r"\b(student|learning|studying)\b", "Students or learners", 0.8, "Student indicators"),
]

# Context detection patterns
CONTEXT_PATTERNS: list[tuple[str, AssumptionCategory, str, float, str]] = [
    (r"\b(company|corporate|enterprise|business|work)\b", AssumptionCategory.CONTEXT, "Business/corporate context", 0.75, "Business context indicators"),
    (r"\b(startup|entrepreneurial)\b", AssumptionCategory.CONTEXT, "Startup environment", 0.8, "Startup indicators"),
    (r"\b(academic|research|university|study|paper)\b", AssumptionCategory.CONTEXT, "Academic/research context", 0.85, "Academic indicators"),
    (r"\b(personal|myself|my own)\b", AssumptionCategory.CONTEXT, "Personal/individual context", 0.7, "Personal indicators"),
]

# Format assumptions by intent
FORMAT_ASSUMPTIONS: dict[IntentType, tuple[str, float, str]] = {
    IntentType.EMAIL_WRITING: ("Standard email format with greeting, body, and closing", 0.9, "Standard email structure"),
    IntentType.CODE_GENERATION: ("Clean, documented code with proper formatting", 0.85, "Code best practices"),
    IntentType.IMAGE_GENERATION: ("High-quality digital image", 0.8, "Standard image output"),
    IntentType.SUMMARIZATION: ("Concise summary highlighting key points", 0.85, "Summary best practices"),
    IntentType.TRANSLATION: ("Accurate translation preserving meaning and tone", 0.9, "Translation standards"),
    IntentType.CREATIVE_WRITING: ("Narrative prose with proper structure", 0.8, "Creative writing conventions"),
    IntentType.QUESTION_ANSWERING: ("Direct answer with supporting explanation", 0.85, "Q&A format"),
    IntentType.ANALYSIS: ("Structured analysis with clear sections", 0.8, "Analysis format"),
}


def generate_assumptions(
    text: str,
    intent: IntentType,
    entities: list[Entity],
    context: str | None = None
) -> list[Assumption]:
    """Generate assumptions about the user's intent based on analysis."""
    
    full_text = text.lower()
    if context:
        full_text = f"{full_text} {context.lower()}"
    
    assumptions: list[Assumption] = []
    categories_covered: set[AssumptionCategory] = set()
    
    # Check tone patterns
    for pattern, assumption_text, confidence, reasoning in TONE_PATTERNS:
        if re.search(pattern, full_text, re.IGNORECASE):
            assumptions.append(Assumption(
                category=AssumptionCategory.TONE,
                value=assumption_text,
                confidence=confidence,
                reasoning=reasoning
            ))
            categories_covered.add(AssumptionCategory.TONE)
            break
    
    # Check audience patterns
    for pattern, assumption_text, confidence, reasoning in AUDIENCE_PATTERNS:
        if re.search(pattern, full_text, re.IGNORECASE):
            assumptions.append(Assumption(
                category=AssumptionCategory.AUDIENCE,
                value=assumption_text,
                confidence=confidence,
                reasoning=reasoning
            ))
            categories_covered.add(AssumptionCategory.AUDIENCE)
            break
    
    # Check context patterns
    for pattern, category, assumption_text, confidence, reasoning in CONTEXT_PATTERNS:
        if re.search(pattern, full_text, re.IGNORECASE):
            assumptions.append(Assumption(
                category=category,
                value=assumption_text,
                confidence=confidence,
                reasoning=reasoning
            ))
            categories_covered.add(category)
            break
    
    # Add format assumption based on intent
    if intent in FORMAT_ASSUMPTIONS:
        value, confidence, reasoning = FORMAT_ASSUMPTIONS[intent]
        assumptions.append(Assumption(
            category=AssumptionCategory.FORMAT,
            value=value,
            confidence=confidence,
            reasoning=reasoning
        ))
        categories_covered.add(AssumptionCategory.FORMAT)
    
    # Add default assumptions for missing categories
    if AssumptionCategory.TONE not in categories_covered:
        assumptions.append(Assumption(
            category=AssumptionCategory.TONE,
            value="Neutral, balanced tone",
            confidence=0.6,
            reasoning="No specific tone indicators found"
        ))
    
    if AssumptionCategory.AUDIENCE not in categories_covered:
        assumptions.append(Assumption(
            category=AssumptionCategory.AUDIENCE,
            value="General audience",
            confidence=0.5,
            reasoning="No specific audience indicators found"
        ))
    
    return assumptions