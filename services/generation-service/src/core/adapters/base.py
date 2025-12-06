from abc import ABC, abstractmethod
from typing import Optional
from src.models import AnalysisData, GeneratedPrompt


class BaseAdapter(ABC):
    """Base class for all platform adapters."""
    
    platform_id: str
    platform_name: str
    platform_type: str  # text, image, audio, video
    
    # Intents this adapter supports
    supported_intents: list[str] = []
    
    @abstractmethod
    def generate(self, analysis: AnalysisData, template_content: str) -> GeneratedPrompt:
        """Generate a prompt for this platform."""
        pass
    
    @abstractmethod
    def apply_rules(self, prompt: str) -> str:
        """Apply platform-specific rules to the prompt."""
        pass
    
    def supports_intent(self, intent: str) -> bool:
        """Check if this adapter supports the given intent."""
        return intent in self.supported_intents
    
    def get_default_settings(self) -> dict:
        """Get default settings for this platform."""
        return {}
    
    def _extract_placeholders(self, prompt: str) -> list[dict]:
        """Extract placeholders from the rendered prompt."""
        import re
        placeholders = []
        matches = re.findall(r'\[([A-Z_]+)\]', prompt)
        for match in matches:
            placeholders.append({
                "key": f"[{match}]",
                "name": match,
                "description": f"Replace with {match.lower().replace('_', ' ')}"
            })
        return placeholders
    
    def _render_template(self, template: str, variables: dict) -> str:
        """Render a template with variables using Jinja2."""
        from jinja2 import Template
        
        # Convert variables to template format
        tpl = Template(template)
        rendered = tpl.render(**variables)
        
        return rendered
    
    def _build_variables(self, analysis: AnalysisData) -> dict:
        """Build template variables from analysis data."""
        variables = {}
        
        # Add entities as variables
        for entity in analysis.entities:
            var_name = entity.type.upper()
            variables[var_name] = entity.value
        
        # Add assumptions as variables
        for assumption in analysis.assumptions:
            var_name = assumption.category.upper()
            if var_name not in variables:
                variables[var_name] = assumption.value
        
        # Add placeholders with defaults or bracket notation
        for placeholder in analysis.placeholders:
            var_name = placeholder.name
            if var_name not in variables:
                if placeholder.default:
                    variables[var_name] = placeholder.default
                else:
                    variables[var_name] = f"[{placeholder.name}]"
        
        return variables