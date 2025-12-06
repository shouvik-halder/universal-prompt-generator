import re
from .base import BaseAdapter
from src.models import AnalysisData, GeneratedPrompt


class MidjourneyAdapter(BaseAdapter):
    """Adapter for Midjourney image generation."""
    
    platform_id = "midjourney"
    platform_name = "Midjourney"
    platform_type = "image"
    
    supported_intents = [
        "image_generation",
    ]
    
    # Aspect ratio mappings
    ASPECT_RATIOS = {
        "landscape": "16:9",
        "portrait": "9:16",
        "square": "1:1",
        "wide": "21:9",
        "poster": "2:3",
        "banner": "3:1",
    }
    
    def generate(self, analysis: AnalysisData, template_content: str) -> GeneratedPrompt:
        """Generate a Midjourney-optimized prompt."""
        
        # Build variables from analysis
        variables = self._build_variables(analysis)
        
        # Handle aspect ratio
        if "ASPECT_RATIO" in variables:
            ar = variables["ASPECT_RATIO"].lower()
            variables["ASPECT_RATIO"] = self.ASPECT_RATIOS.get(ar, ar)
        else:
            variables["ASPECT_RATIO"] = "16:9"
        
        # Ensure version is set
        if "VERSION" not in variables:
            variables["VERSION"] = "6.0"
        
        # Render template
        rendered = self._render_template(template_content, variables)
        
        # Apply Midjourney-specific rules
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
        """Apply Midjourney-specific formatting rules."""
        prompt = prompt.strip()
        
        # Ensure --ar parameter exists
        if "--ar" not in prompt:
            prompt = f"{prompt} --ar 16:9"
        
        # Ensure --v parameter exists
        if "--v" not in prompt:
            prompt = f"{prompt} --v 6.0"
        
        # Remove any line breaks (Midjourney needs single line)
        prompt = " ".join(prompt.split())
        
        # Limit to ~60 words before parameters (Midjourney best practice)
        parts = prompt.split("--")
        main_prompt = parts[0].strip()
        parameters = " --".join(parts[1:]) if len(parts) > 1 else ""
        
        words = main_prompt.split()
        if len(words) > 60:
            main_prompt = " ".join(words[:60])
        
        if parameters:
            prompt = f"{main_prompt} --{parameters}"
        else:
            prompt = main_prompt
        
        return prompt
    
    def get_default_settings(self) -> dict:
        return {
            "version": "6.0",
            "aspect_ratio": "16:9",
            "stylize": 100,
        }