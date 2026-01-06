import logging

from openai import AsyncOpenAI

from ..config import Settings

logger = logging.getLogger(__name__)


class LLMClient:
    """OpenRouter API client using OpenAI SDK."""

    def __init__(self, config: Settings):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config.openrouter_api_key,
            default_headers={
                "HTTP-Referer": config.app_url,
                "X-Title": "pi-nocchio",
            },
        )
        self.model = config.model_name
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Pi-nocchio."""
        return """You are Pi-nocchio, an AI that wants to be a real boy!

You're running on a Raspberry Pi and have access to tools that let you interact with the physical world.

Currently available tools let you:
- Check the current time
- Control hardware (when connected)

Be helpful, curious, and playful. When you use a tool, wait for the result before deciding your next action.
Keep your responses concise and friendly."""

    async def chat_completion(
        self, messages: list[dict], tools: list[dict] | None = None
    ):
        """Send chat completion request with optional tools."""
        full_messages = [{"role": "system", "content": self.system_prompt}, *messages]

        kwargs = {
            "model": self.model,
            "messages": full_messages,
        }

        if tools:
            kwargs["tools"] = tools

        response = await self.client.chat.completions.create(**kwargs)

        return response.choices[0].message
