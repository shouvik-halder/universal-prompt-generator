from .base import BaseAdapter
from src.models import AnalysisData, GeneratedPrompt


class GeminiAdapter(BaseAdapter):
    """Adapter for Google Gemini models."""
    
    platform_id = "gemini"
    platform_name = "Gemini"
    platform_type = "text"
    
    supported_intents = [
        "email_writing",
        "code_generation",
        "summarization",
        "translation",
        "creative_writing",
        "question_answering",
        "analysis",
        "general",
    ]
    
    def generate(self, analysis: AnalysisData, template_content: str) -> GeneratedPrompt:
        """Generate a Gemini-optimized prompt."""
        
        # Build variables from analysis
        variables = self._build_variables(analysis)
        
        # Render template
        rendered = self._render_template(template_content, variables)
        
        # Apply Gemini-specific rules
        final_prompt = self.apply_rules(rendered)
        
        # Extract remaining placeholders
        placeholders = self._extract_placeholders(final_prompt)
        
        return GeneratedPrompt(
            platform=self.platform_id,
            platform_name=self.platform_name,
            prompt=final_prompt,
            placeholders=placeholders,
            settings=self.get_default_settings()
        )
    
    def apply_rules(self, prompt: str) -> str:
        """Apply Gemini-specific formatting rules."""
        # Add Gemini-specific instructions if not present
        safety_note = "\n\nImportant: If you're uncertain about any information, clearly state your uncertainty. Do not invent or fabricate details."
        
        if "uncertain" not in prompt.lower() and "do not invent" not in prompt.lower():
            prompt = prompt + safety_note
        
        return prompt.strip()
    
    def get_default_settings(self) -> dict:
        return {
            "model": "gemini-pro",
            "temperature": 0.7,
            "max_tokens": 2000,
        }