import asyncio
import logging

from .agent.loop import AgentLoop
from .config import get_settings
from .utils.logger import setup_logging


def main():
    """Main entry point for Pi-nocchio."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Pi-nocchio...")

    try:
        config = get_settings()
    except Exception as e:
        print(f"\nError loading configuration: {e}")
        print("Make sure you have a .env file with OPENROUTER_API_KEY set.\n")
        return

    agent = AgentLoop(config)

    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Shutting down Pi-nocchio...")


if __name__ == "__main__":
    main()
