import asyncio
import logging

from .agent.loop import AgentLoop
from .config import get_settings
from .hardware.gpio import cleanup_hardware, init_hardware
from .utils.colors import print_banner
from .utils.logger import setup_logging


def main():
    """Main entry point for Pi-nocchio."""
    # Try to get log level from config, fall back to INFO if config fails
    try:
        config = get_settings()
        log_level = config.log_level
    except Exception:
        log_level = "INFO"
        config = None

    setup_logging(log_level)
    logger = logging.getLogger(__name__)

    # If config loading failed earlier, try again and handle error
    if config is None:
        try:
            config = get_settings()
        except Exception as e:
            print(f"\nError loading configuration: {e}")
            print("Make sure you have a .env file with OPENROUTER_API_KEY set.\n")
            return

    # Print welcome banner
    print_banner(config.agent_name)

    logger.info(f"Starting {config.agent_name}...")

    # Initialize GPIO hardware
    logger.info("Initializing GPIO hardware...")
    init_hardware()

    agent = AgentLoop(config)

    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Shutting down Pi-nocchio...")
    finally:
        # Clean up GPIO resources
        cleanup_hardware()


if __name__ == "__main__":
    main()
