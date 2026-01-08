"""GPIO hardware abstraction layer using gpiozero."""

import logging
from pathlib import Path

import yaml
from gpiozero import LED, MotionSensor, TonalBuzzer

logger = logging.getLogger(__name__)

# Global registry of hardware components
_hardware_registry: dict[str, LED | MotionSensor | TonalBuzzer] = {}
_initialized = False


def _load_gpio_config() -> dict:
    """Load GPIO pin configuration from config/gpio_pins.yaml."""
    config_path = Path("config/gpio_pins.yaml")

    if not config_path.exists():
        logger.warning("GPIO config file not found at config/gpio_pins.yaml")
        return {}

    with open(config_path) as f:
        config = yaml.safe_load(f)
        return config or {}


def init_hardware():
    """Initialize all GPIO hardware from config."""
    global _initialized
    if _initialized:
        return

    config = _load_gpio_config()

    if not config:
        logger.warning("No GPIO configuration found - GPIO tools will not work")
        return

    # Initialize LEDs
    leds = config.get("leds", {})
    for name, pin in leds.items():
        try:
            _hardware_registry[f"led_{name}"] = LED(pin)
            logger.info(f"Initialized LED '{name}' on GPIO {pin}")
        except Exception as e:
            logger.error(f"Failed to initialize LED '{name}' on GPIO {pin}: {e}")

    # Initialize emotion LEDs (individual colored LEDs for emotional expression)
    emotion_leds = config.get("emotion_leds", {})
    for emotion, pin in emotion_leds.items():
        try:
            _hardware_registry[f"emotion_{emotion}"] = LED(pin)
            logger.info(f"Initialized emotion LED '{emotion}' on GPIO {pin}")
        except Exception as e:
            logger.error(f"Failed to initialize emotion LED '{emotion}' on GPIO {pin}: {e}")

    # Initialize speakers (speaker modules with amplifiers for tones/melodies)
    buzzers = config.get("buzzers", {})
    for name, pin in buzzers.items():
        try:
            _hardware_registry[f"buzzer_{name}"] = TonalBuzzer(pin)
            logger.info(f"Initialized speaker '{name}' on GPIO {pin}")
        except Exception as e:
            logger.error(f"Failed to initialize speaker '{name}' on GPIO {pin}: {e}")

    # Initialize motion sensors
    motion_sensors = config.get("motion_sensors", {})
    for name, pin in motion_sensors.items():
        try:
            _hardware_registry[f"motion_{name}"] = MotionSensor(pin)
            logger.info(f"Initialized motion sensor '{name}' on GPIO {pin}")
        except Exception as e:
            logger.error(f"Failed to initialize motion sensor '{name}' on GPIO {pin}: {e}")

    _initialized = True


def get_led(name: str) -> LED:
    """Get LED by name."""
    key = f"led_{name}"
    if key not in _hardware_registry:
        raise ValueError(
            f"LED '{name}' not found. Check config/gpio_pins.yaml and ensure hardware is initialized."
        )
    return _hardware_registry[key]


def get_emotion_led(emotion: str) -> LED:
    """Get emotion LED by emotion name."""
    key = f"emotion_{emotion}"
    if key not in _hardware_registry:
        raise ValueError(
            f"Emotion LED '{emotion}' not found. Check config/gpio_pins.yaml and ensure hardware is initialized."
        )
    return _hardware_registry[key]


def get_buzzer(name: str) -> TonalBuzzer:
    """Get buzzer by name."""
    key = f"buzzer_{name}"
    if key not in _hardware_registry:
        raise ValueError(
            f"Buzzer '{name}' not found. Check config/gpio_pins.yaml and ensure hardware is initialized."
        )
    return _hardware_registry[key]


def get_motion_sensor(name: str) -> MotionSensor:
    """Get motion sensor by name."""
    key = f"motion_{name}"
    if key not in _hardware_registry:
        raise ValueError(
            f"Motion sensor '{name}' not found. Check config/gpio_pins.yaml and ensure hardware is initialized."
        )
    return _hardware_registry[key]


def cleanup_hardware():
    """Clean up all GPIO resources."""
    for component in _hardware_registry.values():
        try:
            component.close()
        except Exception as e:
            logger.error(f"Error cleaning up GPIO component: {e}")
    _hardware_registry.clear()
