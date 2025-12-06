from .base import BaseAdapter
from src.models import AnalysisData, GeneratedPrompt


class ChatGPTAdapter(BaseAdapter):
    """Adapter for ChatGPT/OpenAI GPT models."""
    
    platform_id = "chatgpt"
    platform_name = "ChatGPT"
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
        """Generate a ChatGPT-optimized prompt."""
        
        # Build variables from analysis
        variables = self._build_variables(analysis)
        
        # Render template
        rendered = self._render_template(template_content, variables)
        
        # Apply ChatGPT-specific rules
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
        """Apply ChatGPT-specific formatting rules."""
        # Ensure prompt doesn't exceed reasonable length
        if len(prompt) > 12000:
            prompt = prompt[:12000] + "..."
        
        return prompt.strip()
    
    def get_default_settings(self) -> dict:
        return {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
        }