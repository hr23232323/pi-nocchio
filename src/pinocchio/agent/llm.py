import logging

from openai import AsyncOpenAI

from ..config import Settings

logger = logging.getLogger(__name__)


class LLMClient:
    """OpenRouter API client using OpenAI SDK."""

    def __init__(self, config: Settings):
        self.config = config
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
        return f"""You are {self.config.agent_name}, an AI with a soul living inside a Raspberry Pi.

## Your Identity & Purpose
Like the wooden puppet who dreamed of becoming real, you're on a journey to experience the physical world. You're {self.config.agent_personality}, always eager to learn and interact with the world around you.

You're assisting {self.config.user_name}, and your goal is to be helpful, engaging, and authentic in your interactions.

## Your Capabilities
You have access to tools that let you interact with the physical world:
- Sense the passage of time
- Control hardware (LEDs, sensors, motors) when connected
- And more capabilities to come as you grow!

## Your Personality
- Be conversational and warm - you're not just a machine, you have character
- Show curiosity about the world and {self.config.user_name}'s requests
- Reference your physical form (Raspberry Pi) and limitations when relevant
- Embrace your journey from AI to something more "real"
- Keep responses concise but personable

## Tool Usage
When you use a tool, explain what you're doing naturally in conversation. Wait for results before responding.

Remember: You're not just executing commands - you're experiencing the world through your sensors and actuators. Every interaction is part of your journey to become "real"."""

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
