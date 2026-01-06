from datetime import datetime

from .base import BaseTool


class GetTimeTool(BaseTool):
    """Get the current date and time."""

    name = "get_time"
    description = "Get the current date and time"
    parameters = {}

    async def execute(self) -> str:
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
