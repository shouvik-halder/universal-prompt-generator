import os
from pathlib import Path
from typing import Optional
import yaml

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Template
from src.config import settings


class TemplateLoader:
    """Loads templates from database or files."""
    
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session
        self.templates_dir = Path(settings.templates_dir)
        self._file_cache: dict[str, dict] = {}
    
    async def get_template(
        self,
        platform_id: str,
        intent_id: str,
        variant: str = "default"
    ) -> Optional[str]:
        """
        Get a template by platform, intent, and variant.
        First tries database, then falls back to files.
        """
        # Try database first
        if self.session:
            template = await self._get_from_db(platform_id, intent_id, variant)
            if template:
                return template.content
        
        # Fall back to files
        return self._get_from_file(platform_id, intent_id, variant)
    
    async def _get_from_db(
        self,
        platform_id: str,
        intent_id: str,
        variant: str
    ) -> Optional[Template]:
        """Get template from database."""
        query = select(Template).where(
            Template.platform_id == platform_id,
            Template.intent_id == intent_id,
            Template.variant == variant,
            Template.is_active == True
        ).order_by(Template.version.desc()).limit(1)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    def _get_from_file(
        self,
        platform_id: str,
        intent_id: str,
        variant: str
    ) -> Optional[str]:
        """Get template from file system."""
        # Check cache first
        cache_key = f"{platform_id}/{intent_id}/{variant}"
        if cache_key in self._file_cache:
            return self._file_cache[cache_key].get("content")
        
        # Look for file
        file_path = self.templates_dir / platform_id / intent_id / f"{variant}.yaml"
        
        if not file_path.exists():
            # Try default variant
            file_path = self.templates_dir / platform_id / intent_id / "default.yaml"
        
        if not file_path.exists():
            return None
        
        # Load and cache
        with open(file_path) as f:
            data = yaml.safe_load(f)
            self._file_cache[cache_key] = data
            return data.get("content")
    
    def get_default_template(self, platform_id: str, intent_id: str) -> str:
        """Get a default template if no specific template exists."""
        return DEFAULT_TEMPLATES.get(platform_id, {}).get(intent_id, DEFAULT_FALLBACK)


# Default templates as fallback
DEFAULT_FALLBACK = """You are a helpful AI assistant.

Task: {{ TASK | default('[Describe your task]') }}

Please provide a thorough and helpful response.
"""

DEFAULT_TEMPLATES = {
    "chatgpt": {
        "email_writing": """You are an expert email writer with years of experience in professional communication.

## Task
Write a {{ TONE | default('professional') }} email to {{ RECIPIENT | default('[RECIPIENT_NAME]') }} regarding: {{ SUBJECT | default('[EMAIL_SUBJECT]') }}

## Requirements
- Use a {{ TONE | default('professional') }} tone
- Be clear and concise
- Include a compelling subject line
- End with a clear call to action

## Structure
1. Subject line suggestion
2. Greeting
3. Opening (purpose/context)
4. Body (main content)
5. Closing (call to action)
6. Sign-off

{% if CONTEXT %}
## Additional Context
{{ CONTEXT }}
{% endif %}

Write the complete email now.
""",
        "code_generation": """You are an expert {{ LANGUAGE | default('[PROGRAMMING_LANGUAGE]') }} developer with deep knowledge of best practices and clean code principles.

## Task
{{ TASK_DESCRIPTION | default('[Describe what the code should do]') }}

## Requirements
- Language: {{ LANGUAGE | default('[PROGRAMMING_LANGUAGE]') }}
{% if FRAMEWORK %}- Framework: {{ FRAMEWORK }}{% endif %}
- Write clean, readable, well-commented code
- Include error handling
- Follow best practices

## Expected Output
1. Complete, working code
2. Brief explanation of the approach
3. Usage example

Think step by step before writing the code.
""",
        "summarization": """You are an expert at summarizing content while preserving key information.

## Task
Summarize the following content in a {{ LENGTH | default('concise') }} manner.

## Content to Summarize
{{ CONTENT | default('[PASTE CONTENT HERE]') }}

## Requirements
- Capture all key points
- Maintain accuracy
- Use {{ FORMAT | default('paragraph') }} format
- Be {{ LENGTH | default('concise') }} but comprehensive

Provide the summary now.
""",
    },
    "claude": {
        "email_writing": """<task>
Write a {{ TONE | default('professional') }} email to {{ RECIPIENT | default('[RECIPIENT_NAME]') }} about {{ SUBJECT | default('[EMAIL_SUBJECT]') }}.
</task>

<context>
You are an expert email writer. The email should be well-structured and appropriate for the intended recipient.
{% if CONTEXT %}Additional context: {{ CONTEXT }}{% endif %}
</context>

<requirements>
- Use a {{ TONE | default('professional') }} tone
- Be clear and concise
- Include a subject line suggestion
- End with a clear call to action
</requirements>

<format>
1. Suggested subject line
2. Email content with proper greeting and closing
</format>

<reflection>
Before writing, consider the recipient's perspective and what would make this email most effective.
</reflection>
""",
        "code_generation": """<task>
{{ TASK_DESCRIPTION | default('[Describe what the code should do]') }}
</task>

<context>
You are an expert {{ LANGUAGE | default('[PROGRAMMING_LANGUAGE]') }} developer. Write production-quality code.
</context>

<requirements>
<requirement>Language: {{ LANGUAGE | default('[PROGRAMMING_LANGUAGE]') }}</requirement>
{% if FRAMEWORK %}<requirement>Framework: {{ FRAMEWORK }}</requirement>{% endif %}
<requirement>Write clean, documented code</requirement>
<requirement>Include error handling</requirement>
<requirement>Follow best practices</requirement>
</requirements>

<format>
1. Brief approach explanation
2. Complete code with comments
3. Usage example
</format>

<reflection>
Before writing, consider edge cases, error handling, and maintainability.
</reflection>
""",
    },
    "gemini": {
        "email_writing": """**Role:** Expert Email Writer

**Task:** Write a {{ TONE | default('professional') }} email to {{ RECIPIENT | default('[RECIPIENT_NAME]') }} regarding {{ SUBJECT | default('[EMAIL_SUBJECT]') }}.

**Requirements:**
• Use a {{ TONE | default('professional') }} tone
• Be clear and direct
• Include a subject line
• End with a call to action

**Output Format:**
1. **Subject:** Your suggested subject line
2. **Email:** The complete email

{% if CONTEXT %}
**Additional Context:** {{ CONTEXT }}
{% endif %}

**Important:** State any assumptions you make. Do not invent details not provided.
""",
    },
    "midjourney": {
        "image_generation": """{{ SUBJECT | default('[MAIN SUBJECT]') }}{% if STYLE %}, {{ STYLE }} style{% endif %}{% if MOOD %}, {{ MOOD }} mood{% endif %}{% if LIGHTING %}, {{ LIGHTING }} lighting{% endif %}, high quality, detailed --ar {{ ASPECT_RATIO | default('16:9') }} --v {{ VERSION | default('6.0') }}{% if STYLIZE %} --stylize {{ STYLIZE }}{% endif %}
""",
    },
}