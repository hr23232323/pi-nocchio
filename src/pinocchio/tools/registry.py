import inspect
import logging

from ..config import get_tools_config
from .base import BaseTool

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Manages tool discovery, filtering, and execution."""

    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self._discover_tools()

    def _discover_tools(self):
        """Auto-discover and register all tool classes."""
        from . import gpio_tools, utility_tools, voice_tools

        tools_config = get_tools_config()
        enabled_tools = tools_config.get("tools", {})

        modules = [utility_tools, gpio_tools, voice_tools]

        for module in modules:
            for name in dir(module):
                obj = getattr(module, name)

                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BaseTool)
                    and obj != BaseTool
                ):
                    try:
                        tool = obj()

                        if tool.name in enabled_tools and enabled_tools[tool.name].get(
                            "enabled", False
                        ):
                            self.tools[tool.name] = tool
                            logger.info(f"Registered tool: {tool.name}")
                        else:
                            logger.debug(f"Tool {tool.name} is disabled in config")

                    except Exception as e:
                        logger.warning(f"Failed to instantiate tool {name}: {e}")

    def get_tool_definitions(self) -> list[dict]:
        """Get all enabled tools in OpenAI function format."""
        return [tool.to_openai_function() for tool in self.tools.values()]

    async def execute(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool by name with given arguments."""
        if tool_name not in self.tools:
            return f"Error: Unknown tool '{tool_name}'"

        try:
            result = await self.tools[tool_name].execute(**arguments)
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return f"Error executing {tool_name}: {str(e)}"
