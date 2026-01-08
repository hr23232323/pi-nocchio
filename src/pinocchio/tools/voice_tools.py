"""Voice-related tools for speech synthesis using Piper TTS."""

import logging
import os
import subprocess
import tempfile
from pathlib import Path

from ..config import get_settings
from .base import BaseTool, ToolParameter

logger = logging.getLogger(__name__)


class SpeakTool(BaseTool):
    """Speak text aloud using Piper (local neural text-to-speech)."""

    name = "speak"
    description = (
        "Speak text aloud through the speaker using natural-sounding voice synthesis. "
        "Uses Piper - a fast, local, offline neural TTS system running directly on the Pi. "
        "Use this to verbally communicate with the user, express thoughts out loud, "
        "or provide audio feedback. The voice will sound natural and human-like. "
        "Perfect for greetings, responses, announcements, or any verbal communication!"
    )
    parameters = {
        "text": ToolParameter(
            type="string",
            description="The text to speak aloud",
        ),
    }

    async def execute(self, text: str) -> str:
        try:
            settings = get_settings()

            # Expand model path
            model_dir = Path(settings.piper_model_path).expanduser()
            voice_name = settings.piper_voice
            model_file = model_dir / f"{voice_name}.onnx"

            # Check if Piper is installed
            piper_check = subprocess.run(
                ["which", "piper"],
                capture_output=True,
            )

            if piper_check.returncode != 0:
                return "❌ Piper not installed. Run setup script or install: pip install piper-tts"

            # Check if voice model exists
            if not model_file.exists():
                return (
                    f"❌ Voice model '{voice_name}' not found at {model_file}. "
                    f"Download voices from: https://github.com/rhasspy/piper/releases"
                )

            logger.debug(f"Generating speech for: {text[:50]}...")

            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = Path(temp_file.name)

            # Run Piper to generate speech
            # Echo text to stdin and output to file
            piper_process = subprocess.run(
                ["piper", "--model", str(model_file), "--output_file", str(temp_path)],
                input=text,
                text=True,
                capture_output=True,
                timeout=30,
            )

            if piper_process.returncode != 0:
                logger.error(f"Piper error: {piper_process.stderr}")
                temp_path.unlink(missing_ok=True)
                return f"❌ Piper TTS failed: {piper_process.stderr}"

            # Play audio using aplay (standard on Raspberry Pi)
            logger.debug(f"Playing audio file: {temp_path}")
            play_process = subprocess.run(
                ["aplay", "-q", str(temp_path)],
                capture_output=True,
                timeout=30,
            )

            if play_process.returncode != 0:
                logger.error(f"aplay error: {play_process.stderr}")
                temp_path.unlink(missing_ok=True)
                return "❌ Audio playback failed. Is aplay installed?"

            # Clean up temp file
            temp_path.unlink(missing_ok=True)

            # Return confirmation
            preview = text[:50] + "..." if len(text) > 50 else text
            return f'🗣️ Spoke: "{preview}"'

        except subprocess.TimeoutExpired:
            logger.error("TTS operation timed out")
            return "❌ Speech generation timed out"
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return f"❌ Failed to speak: {str(e)}"
