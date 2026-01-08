import asyncio

from ..hardware.gpio import get_buzzer, get_emotion_led, get_led
from .base import BaseTool, ToolParameter

# Musical note frequencies (in Hz) for melodies
NOTES = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "F5": 698.46,
    "G5": 783.99,
    "A5": 880.00,
    "REST": 0,  # Silence/rest
}


class ToggleLEDTool(BaseTool):
    """Control an LED (requires GPIO hardware)."""

    name = "toggle_led"
    description = "Turn an LED on or off. Available LEDs: 'status'"
    parameters = {
        "led_name": ToolParameter(
            type="string",
            description="Name of the LED (e.g., 'status')",
        ),
        "state": ToolParameter(
            type="string", description="Desired state: 'on' or 'off'", enum=["on", "off"]
        ),
    }

    async def execute(self, led_name: str, state: str) -> str:
        try:
            led = get_led(led_name)

            if state == "on":
                led.on()
                return f"✅ LED '{led_name}' is now ON"
            else:
                led.off()
                return f"✅ LED '{led_name}' is now OFF"

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to control LED '{led_name}': {str(e)}"


class CheckMotionTool(BaseTool):
    """Check motion sensor (requires GPIO hardware)."""

    name = "check_motion"
    description = "Check if motion is detected by a PIR sensor"
    parameters = {
        "sensor_name": ToolParameter(
            type="string", description="Name of the motion sensor"
        )
    }

    async def execute(self, sensor_name: str) -> str:
        return f"Motion sensor '{sensor_name}' would be checked (GPIO not implemented yet)"


class ExpressEmotionTool(BaseTool):
    """Express an emotion using colored LEDs."""

    name = "express_emotion"
    description = (
        "Express an emotional state by lighting up a colored LED. Pi-nocchio uses colors to show how it feels! "
        "Available emotions: "
        "'excited' (red LED - excitement, alerts, high energy), "
        "'happy' (green LED - happiness, success, calm, contentment), "
        "'curious' (yellow LED - thinking, wondering, processing), "
        "'neutral' (all LEDs off - calm, idle state). "
        "Only one emotion can be shown at a time - the previous emotion LED will turn off."
    )
    parameters = {
        "emotion": ToolParameter(
            type="string",
            description="The emotion to express: 'excited', 'happy', 'curious', or 'neutral'",
            enum=["excited", "happy", "curious", "neutral"],
        ),
    }

    async def execute(self, emotion: str) -> str:
        try:
            # Turn off all emotion LEDs first
            for emo in ["excited", "happy", "curious"]:
                try:
                    led = get_emotion_led(emo)
                    led.off()
                except ValueError:
                    pass  # LED not configured, skip

            # Handle neutral state
            if emotion == "neutral":
                return "😌 Feeling neutral - all emotion LEDs off"

            # Turn on the requested emotion LED
            led = get_emotion_led(emotion)
            led.on()

            # Emotional responses
            emotion_messages = {
                "excited": "🔴 Feeling excited! Red LED is glowing with energy!",
                "happy": "🟢 Feeling happy! Green LED shining with joy!",
                "curious": "🟡 Feeling curious! Yellow LED lit up - I'm thinking!",
            }

            return emotion_messages.get(emotion, f"✅ Expressing {emotion}")

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to express emotion '{emotion}': {str(e)}"


class PulseEmotionTool(BaseTool):
    """Pulse an emotion LED with a breathing effect."""

    name = "pulse_emotion"
    description = (
        "Pulse/breathe an emotion LED to show intensity of feeling. Creates a smooth fade in/out effect. "
        "Available emotions: 'excited' (red), 'happy' (green), 'curious' (yellow)"
    )
    parameters = {
        "emotion": ToolParameter(
            type="string",
            description="The emotion to pulse: 'excited', 'happy', or 'curious'",
            enum=["excited", "happy", "curious"],
        ),
        "duration": ToolParameter(
            type="number",
            description="How long to pulse in seconds (default: 2.0)",
        ),
        "pulses": ToolParameter(
            type="number",
            description="Number of pulses (default: 3)",
        ),
    }

    async def execute(self, emotion: str, duration: float = 2.0, pulses: int = 3) -> str:
        try:
            # Turn off other emotion LEDs
            for emo in ["excited", "happy", "curious"]:
                if emo != emotion:
                    try:
                        led = get_emotion_led(emo)
                        led.off()
                    except ValueError:
                        pass

            led = get_emotion_led(emotion)

            # Pulse the LED
            led.pulse(fade_in_time=duration / 2, fade_out_time=duration / 2, n=pulses, background=False)

            # Turn on after pulsing
            led.on()

            emotion_messages = {
                "excited": f"💓 Pulsing with excitement! Red LED pulsed {pulses} times",
                "happy": f"💚 Radiating happiness! Green LED pulsed {pulses} times",
                "curious": f"💛 Pondering intensely! Yellow LED pulsed {pulses} times",
            }

            return emotion_messages.get(emotion, f"✅ Pulsed {emotion} LED {pulses} times")

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to pulse emotion '{emotion}': {str(e)}"


class BlinkEmotionTool(BaseTool):
    """Blink an emotion LED on and off rapidly."""

    name = "blink_emotion"
    description = (
        "Blink an emotion LED on and off to show bursts of feeling or get attention. "
        "Available emotions: 'excited' (red), 'happy' (green), 'curious' (yellow)"
    )
    parameters = {
        "emotion": ToolParameter(
            type="string",
            description="The emotion to blink: 'excited', 'happy', or 'curious'",
            enum=["excited", "happy", "curious"],
        ),
        "times": ToolParameter(
            type="number",
            description="Number of blinks (default: 5)",
        ),
        "speed": ToolParameter(
            type="number",
            description="Blink speed in seconds (default: 0.3)",
        ),
    }

    async def execute(self, emotion: str, times: int = 5, speed: float = 0.3) -> str:
        try:
            # Turn off other emotion LEDs
            for emo in ["excited", "happy", "curious"]:
                if emo != emotion:
                    try:
                        led = get_emotion_led(emo)
                        led.off()
                    except ValueError:
                        pass

            led = get_emotion_led(emotion)

            # Blink pattern
            for _ in range(times):
                led.on()
                await asyncio.sleep(speed)
                led.off()
                await asyncio.sleep(speed)

            # Leave it on at the end
            led.on()

            emotion_messages = {
                "excited": f"⚡ Bursting with excitement! Red LED blinked {times} times",
                "happy": f"✨ Sparkling with joy! Green LED blinked {times} times",
                "curious": f"💡 Ideas flashing! Yellow LED blinked {times} times",
            }

            return emotion_messages.get(emotion, f"✅ Blinked {emotion} LED {times} times")

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to blink emotion '{emotion}': {str(e)}"


class PlayToneTool(BaseTool):
    """Play a tone at a specific frequency through the speaker."""

    name = "play_tone"
    description = (
        "Play a tone/sound at a specific frequency through the speaker for a duration. "
        "Lower frequencies (200-400 Hz) = deep sounds. "
        "Mid frequencies (400-800 Hz) = normal tones. "
        "Higher frequencies (800-2000 Hz) = high-pitched beeps. "
        "Use this for alerts, notifications, or simple sounds!"
    )
    parameters = {
        "frequency": ToolParameter(
            type="number",
            description="Frequency in Hz (200-2000). Example: 440 = musical note A4",
        ),
        "duration": ToolParameter(
            type="number",
            description="Duration in seconds (default: 0.5)",
        ),
    }

    async def execute(self, frequency: float, duration: float = 0.5) -> str:
        try:
            buzzer = get_buzzer("main")

            # Play the tone
            buzzer.play(frequency)
            await asyncio.sleep(duration)
            buzzer.stop()

            return f"🔊 Played {frequency} Hz tone for {duration}s"

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to play tone: {str(e)}"


class PlayMelodyTool(BaseTool):
    """Play a simple melody using musical notes."""

    name = "play_melody"
    description = (
        "Play a melody using musical notes! Each note is a string like 'C4', 'E4', 'G5'. "
        "Available notes: C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, REST (silence). "
        "Example: ['C4', 'E4', 'G4', 'C5'] plays a C major chord ascending. "
        "Use 'REST' for pauses in the melody. Great for alerts, celebrations, or musical expression!"
    )
    parameters = {
        "notes": ToolParameter(
            type="array",
            description="Array of note names like ['C4', 'E4', 'G4'] or ['C4', 'REST', 'E4']",
        ),
        "note_duration": ToolParameter(
            type="number",
            description="Duration of each note in seconds (default: 0.3)",
        ),
    }

    async def execute(self, notes: list[str], note_duration: float = 0.3) -> str:
        try:
            buzzer = get_buzzer("main")

            played_notes = []
            for note in notes:
                note_upper = note.upper()

                if note_upper not in NOTES:
                    return f"❌ Unknown note '{note}'. Available: C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, REST"

                freq = NOTES[note_upper]

                if freq == 0:  # REST
                    buzzer.stop()
                else:
                    buzzer.play(freq)

                await asyncio.sleep(note_duration)
                played_notes.append(note_upper)

            buzzer.stop()

            note_list = ", ".join(played_notes)
            return f"🎵 Played melody: {note_list}"

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to play melody: {str(e)}"


class BeepPatternTool(BaseTool):
    """Create custom beep patterns for alerts and notifications."""

    name = "beep_pattern"
    description = (
        "Create a custom beep pattern using short/long beeps and pauses. "
        "Pattern examples: "
        "'short-short-long' = two quick beeps + one long beep (like morse code S-O-S), "
        "'long-pause-long' = alert pattern, "
        "'short-short-short' = triple beep notification. "
        "Use for: alerts, confirmations, alarms, attention-getting, morse code!"
    )
    parameters = {
        "pattern": ToolParameter(
            type="string",
            description="Pattern string like 'short-short-long' or 'long-pause-short-pause-short'",
        ),
        "frequency": ToolParameter(
            type="number",
            description="Beep frequency in Hz (default: 800)",
        ),
    }

    async def execute(self, pattern: str, frequency: float = 800) -> str:
        try:
            buzzer = get_buzzer("main")

            # Define timing for pattern elements
            timings = {
                "short": 0.15,  # Short beep
                "long": 0.5,  # Long beep
                "pause": 0.3,  # Pause/silence
            }

            parts = pattern.lower().split("-")

            for part in parts:
                part = part.strip()

                if part == "pause":
                    buzzer.stop()
                    await asyncio.sleep(timings["pause"])
                elif part in ["short", "long"]:
                    buzzer.play(frequency)
                    await asyncio.sleep(timings[part])
                    buzzer.stop()
                    await asyncio.sleep(0.1)  # Small gap between beeps
                else:
                    return f"❌ Unknown pattern element '{part}'. Use: short, long, pause"

            buzzer.stop()

            return f"🔔 Played pattern: {pattern}"

        except ValueError as e:
            return f"❌ Error: {str(e)}"
        except Exception as e:
            return f"❌ Failed to play beep pattern: {str(e)}"
