"""Voice listener with wake word detection and speech-to-text."""

import json
import logging
import queue
import time
from pathlib import Path

import pyaudio
import vosk

from ..config import get_settings
from ..utils.colors import Colors

logger = logging.getLogger(__name__)


class VoiceListener:
    """Listens for wake word and captures speech using Vosk."""

    def __init__(self, wake_word: str = "pinocchio"):
        """Initialize voice listener.

        Args:
            wake_word: Wake word to listen for (default: "pinocchio")
        """
        self.wake_word = wake_word.lower()
        self.model = None
        self.recognizer = None
        self.audio_queue = queue.Queue()

        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 4000
        self.silence_limit = 1.5  # Seconds of silence before stopping
        self.silence_threshold = 500  # RMS threshold for silence detection

        self._initialize_model()

    def _initialize_model(self):
        """Initialize Vosk model."""
        settings = get_settings()
        model_path = Path(settings.vosk_model_path).expanduser()

        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}. "
                f"Download a model from https://alphacephei.com/vosk/models and "
                f"extract it to {model_path}, or run the setup script."
            )

        logger.info(f"Loading Vosk model from {model_path}...")
        self.model = vosk.Model(str(model_path))
        self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
        logger.info("Vosk model loaded successfully")

    def _get_rms(self, data: bytes) -> float:
        """Calculate RMS (root mean square) of audio data."""
        import array

        count = len(data) / 2
        shorts = array.array("h", data)
        sum_squares = sum(s**2 for s in shorts)
        return (sum_squares / count) ** 0.5

    def listen_for_wake_word(self) -> bool:
        """Listen continuously for wake word.

        Returns:
            True if wake word detected, False otherwise
        """
        p = pyaudio.PyAudio()

        try:
            # Open microphone stream
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )

            print(Colors.dim(f"Listening for wake word '{self.wake_word}'..."))

            while True:
                data = stream.read(self.chunk_size, exception_on_overflow=False)

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()

                    if text and self.wake_word in text:
                        print(Colors.green(f"✓ Wake word '{self.wake_word}' detected!"))
                        return True

                # Also check partial results for faster detection
                partial = json.loads(self.recognizer.PartialResult())
                partial_text = partial.get("partial", "").lower()
                if partial_text and self.wake_word in partial_text:
                    print(Colors.green(f"✓ Wake word '{self.wake_word}' detected!"))
                    return True

        except KeyboardInterrupt:
            print(Colors.yellow("\nStopping wake word detection..."))
            return False
        except Exception as e:
            logger.error(f"Error in wake word detection: {e}")
            return False
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            # Reset recognizer for next listening session
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)

    def capture_speech(self) -> str:
        """Capture speech after wake word until silence.

        Returns:
            Transcribed text from speech
        """
        p = pyaudio.PyAudio()

        try:
            # Open microphone stream
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )

            print(Colors.cyan("Listening... (speak now)"))

            # Reset recognizer for clean speech capture
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)

            silence_start = None
            full_text = []

            while True:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                rms = self._get_rms(data)

                # Check for silence
                if rms < self.silence_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > self.silence_limit:
                        # Silence detected, stop listening
                        break
                else:
                    # Reset silence timer when speech detected
                    silence_start = None

                # Process audio with Vosk
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        full_text.append(text)

            # Get final result
            final = json.loads(self.recognizer.FinalResult())
            final_text = final.get("text", "")
            if final_text:
                full_text.append(final_text)

            transcribed = " ".join(full_text).strip()

            if transcribed:
                print(Colors.blue(f"You said: {transcribed}"))
            else:
                print(Colors.dim("(no speech detected)"))

            return transcribed

        except KeyboardInterrupt:
            print(Colors.yellow("\nStopping speech capture..."))
            return ""
        except Exception as e:
            logger.error(f"Error capturing speech: {e}")
            return ""
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            # Reset recognizer for next wake word detection
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)

    def listen_once(self) -> str | None:
        """Listen for wake word, then capture speech.

        Returns:
            Transcribed speech text, or None if interrupted
        """
        # Wait for wake word
        if not self.listen_for_wake_word():
            return None

        # Capture speech
        speech = self.capture_speech()

        if not speech:
            print(Colors.dim("No speech captured, waiting for wake word again..."))
            return ""

        return speech
