from typing import Optional
from .base import BaseAdapter
from .chatgpt import ChatGPTAdapter
from .claude import ClaudeAdapter
from .gemini import GeminiAdapter
from .midjourney import MidjourneyAdapter


class AdapterRegistry:
    """Registry of all available platform adapters."""
    
    _adapters: dict[str, BaseAdapter] = {}
    
    @classmethod
    def register(cls, adapter: BaseAdapter) -> None:
        """Register an adapter."""
        cls._adapters[adapter.platform_id] = adapter
    
    @classmethod
    def get(cls, platform_id: str) -> Optional[BaseAdapter]:
        """Get an adapter by platform ID."""
        return cls._adapters.get(platform_id)
    
    @classmethod
    def get_all(cls) -> list[BaseAdapter]:
        """Get all registered adapters."""
        return list(cls._adapters.values())
    
    @classmethod
    def get_for_intent(cls, intent: str) -> list[BaseAdapter]:
        """Get all adapters that support a given intent."""
        return [
            adapter for adapter in cls._adapters.values()
            if adapter.supports_intent(intent)
        ]
    
    @classmethod
    def get_text_adapters(cls) -> list[BaseAdapter]:
        """Get all text-based adapters."""
        return [
            adapter for adapter in cls._adapters.values()
            if adapter.platform_type == "text"
        ]
    
    @classmethod
    def get_image_adapters(cls) -> list[BaseAdapter]:
        """Get all image-based adapters."""
        return [
            adapter for adapter in cls._adapters.values()
            if adapter.platform_type == "image"
        ]


# Register all adapters
AdapterRegistry.register(ChatGPTAdapter())
AdapterRegistry.register(ClaudeAdapter())
AdapterRegistry.register(GeminiAdapter())
AdapterRegistry.register(MidjourneyAdapter())