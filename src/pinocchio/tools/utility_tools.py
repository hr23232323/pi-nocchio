import asyncio
from datetime import datetime

from .base import BaseTool, ToolParameter


class GetTimeTool(BaseTool):
    """Get the current date and time."""

    name = "get_time"
    description = "Get the current date and time"
    parameters = {}

    async def execute(self) -> str:
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


class WaitTool(BaseTool):
    """Wait/pause for a specified duration."""

    name = "wait"
    description = "Wait or sleep for a specified number of seconds. Useful for creating delays between actions like blinking LEDs."
    parameters = {
        "seconds": ToolParameter(
            type="number",
            description="Number of seconds to wait (can be decimal like 0.5 for half a second)",
        )
    }

    async def execute(self, seconds: float) -> str:
        await asyncio.sleep(seconds)
        return f"⏱️  Waited {seconds} seconds"
