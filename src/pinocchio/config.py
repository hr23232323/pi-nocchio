from pathlib import Path

import yaml
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Main application settings loaded from environment variables."""

    openrouter_api_key: str
    model_name: str = "anthropic/claude-3.5-sonnet"
    app_url: str = "https://github.com/hr23232323/pi-nocchio"

    # Piper TTS (local text-to-speech)
    piper_voice: str = "en_US-lessac-medium"  # Default voice model
    piper_model_path: str = "~/.local/share/piper/voices"  # Where voice models are stored

    # Personalization
    user_name: str = "Friend"
    agent_name: str = "Pi-nocchio"
    agent_personality: str = "curious and playful"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_tools_config() -> dict:
    """Load tools configuration from config/tools.yaml."""
    config_path = Path("config/tools.yaml")

    if not config_path.exists():
        return {"tools": {}}

    with open(config_path) as f:
        return yaml.safe_load(f) or {"tools": {}}
