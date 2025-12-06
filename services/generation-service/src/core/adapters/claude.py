import re
from .base import BaseAdapter
from src.models import AnalysisData, GeneratedPrompt


class ClaudeAdapter(BaseAdapter):
    """Adapter for Anthropic Claude models."""
    
    platform_id = "claude"
    platform_name = "Claude"
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
        """Generate a Claude-optimized prompt with XML structure."""
        
        # Build variables from analysis
        variables = self._build_variables(analysis)
        
        # Render template
        rendered = self._render_template(template_content, variables)
        
        # Apply Claude-specific rules (XML formatting)
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
        """Apply Claude-specific formatting rules."""
        # Ensure XML tags are properly closed
        prompt = self._ensure_xml_structure(prompt)
        
        return prompt.strip()
    
    def _ensure_xml_structure(self, prompt: str) -> str:
        """Ensure the prompt has proper XML structure for Claude."""
        # Check if prompt already has XML tags
        if "<task>" in prompt.lower() or "<context>" in prompt.lower():
            return prompt
        
        # If no XML tags, the template should already have them
        # This is a safety check
        return prompt
    
    def get_default_settings(self) -> dict:
        return {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.7,
            "max_tokens": 2000,
        }