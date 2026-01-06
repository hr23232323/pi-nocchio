import json
import logging

from ..config import Settings
from ..tools.registry import ToolRegistry
from .llm import LLMClient

logger = logging.getLogger(__name__)


class AgentLoop:
    """Main autonomous agent control loop."""

    def __init__(self, config: Settings):
        self.llm = LLMClient(config)
        self.tool_registry = ToolRegistry()
        self.conversation_history: list[dict] = []
        self.max_history = 20

    async def run(self):
        """Main text-based interaction loop."""
        print("\nPi-nocchio is ready! (Type 'quit' to exit)\n")

        if not self.tool_registry.tools:
            print("Warning: No tools are enabled. Check config/tools.yaml\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("\nPi-nocchio: Goodbye! I'll keep dreaming of being a real boy!")
                    break

                self.conversation_history.append({"role": "user", "content": user_input})

                self._trim_history()

                response_text = await self._agent_reasoning_loop()

                print(f"\nPi-nocchio: {response_text}\n")

            except KeyboardInterrupt:
                print("\n\nPi-nocchio: Goodbye! I'll keep dreaming of being a real boy!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"\nError: {e}\n")

    async def _agent_reasoning_loop(self) -> str:
        """Inner loop for agent reasoning with tool calls."""
        while True:
            response = await self.llm.chat_completion(
                messages=self.conversation_history,
                tools=self.tool_registry.get_tool_definitions(),
            )

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    logger.info(f"Tool call: {tool_call.function.name}")

                    arguments = json.loads(tool_call.function.arguments)

                    print(
                        f"[Using tool: {tool_call.function.name} with args: {arguments}]"
                    )

                    result = await self.tool_registry.execute(
                        tool_call.function.name, arguments
                    )

                    logger.info(f"Tool result: {result}")

                    self.conversation_history.append(
                        {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_call.function.name,
                                        "arguments": tool_call.function.arguments,
                                    },
                                }
                            ],
                        }
                    )

                    self.conversation_history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )

                continue

            assistant_message = response.content or "..."
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            return assistant_message

    def _trim_history(self):
        """Trim conversation history to prevent token overflow."""
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history :]
