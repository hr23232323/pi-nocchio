from ..hardware.gpio import get_led
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
