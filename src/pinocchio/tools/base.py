from abc import ABC, abstractmethod
from typing import Any


class ToolParameter:
    """Definition for a tool parameter."""

    def __init__(
        self,
        type: str,
        description: str,
        enum: list[str] | None = None,
        items: dict | None = None,
    ):
        self.type = type
        self.description = description
        self.enum = enum
        self.items = items  # For array types


class BaseTool(ABC):
    """Base class for all tools that the LLM can use."""

    name: str
    description: str
    parameters: dict[str, ToolParameter]

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool and return result as string."""
        pass

    def to_openai_function(self) -> dict:
        """Convert tool definition to OpenAI function calling format."""
        properties = {}
        for param_name, param in self.parameters.items():
            prop = {
                "type": param.type,
                "description": param.description,
            }
            if param.enum:
                prop["enum"] = param.enum
            if param.items:
                prop["items"] = param.items
            properties[param_name] = prop

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": list(self.parameters.keys()),
                },
            },
        }
