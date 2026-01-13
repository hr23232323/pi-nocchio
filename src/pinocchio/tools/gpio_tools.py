import asyncio

from ..hardware.gpio import get_emotion_led, get_led
from .base import BaseTool, ToolParameter


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
