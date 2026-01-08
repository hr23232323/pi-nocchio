# pi-nocchio

> The "I want to be a real boy" starter kit for LLMs built for Raspberry Pis

Give an LLM a physical body! Pi-nocchio is an autonomous agent system that runs on a Raspberry Pi, enabling LLMs to interact with the real world through sensors and actuators.

**🚀 [Deploy to Raspberry Pi →](DEPLOY.md)**

## Features

- **Personalized AI with Soul** - Give Pi-nocchio a unique personality, name, and purpose
- **Knows Who It's Assisting** - Configure your name so it can build a relationship with you
- Text-based LLM agent with tool-calling capabilities
- Simple custom agent loop (no complex frameworks)
- Easy tool enable/disable via config
- Extensible architecture - just add tool classes!
- Built for Raspberry Pi but runs anywhere Python does

## Quick Start

### 1. Prerequisites

- Python 3.11+
- [uv](https://astral.sh/uv) package manager
- OpenRouter API key ([get one here](https://openrouter.ai/))

### 2. Clone & Setup

```bash
git clone https://github.com/hr23232323/pi-nocchio.git
cd pi-nocchio
```

### 3. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 4. Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenRouter API key
nano .env
```

Add your API key to `.env`:
```bash
OPENROUTER_API_KEY=your_api_key_here
MODEL_NAME=anthropic/claude-3.5-sonnet
```

### 5. Run

```bash
# Option 1: Using uv directly
uv run python -m pinocchio

# Option 2: Using the run script
./scripts/run.sh
```

## Usage

Once running, you'll see a simple CLI interface:

```
Pi-nocchio is ready! (Type 'quit' to exit)

You: What time is it?
[Using tool: get_time with args: {}]

Pi-nocchio: The current time is 2026-01-05 19:30:45
```

Pi-nocchio will autonomously use available tools to answer your questions!

## Project Structure

```
pi-nocchio/
├── pyproject.toml              # Dependencies, metadata
├── .env.example                # Config template
├── README.md
├── .gitignore
├── src/
│   └── pinocchio/
│       ├── __main__.py         # Entry point
│       ├── config.py           # Configuration management
│       ├── agent/
│       │   ├── loop.py         # Main agent control loop
│       │   └── llm.py          # OpenRouter integration
│       ├── tools/
│       │   ├── base.py         # BaseTool abstract class
│       │   ├── registry.py     # Tool discovery & execution
│       │   ├── utility_tools.py # General utility tools (time, etc.)
│       │   └── gpio_tools.py   # GPIO-based tools (LED, sensors)
│       ├── hardware/
│       │   └── gpio.py         # GPIO abstraction (future)
│       └── utils/
│           └── logger.py       # Logging setup
├── config/
│   └── tools.yaml              # Tool enable/disable config
└── scripts/
    └── run.sh                  # Launch script
```

## Adding New Tools

Creating a new tool is simple! Just create a class that inherits from `BaseTool`:

```python
# In src/pinocchio/tools/utility_tools.py (for general tools)
# OR src/pinocchio/tools/gpio_tools.py (for GPIO-based tools)

from .base import BaseTool, ToolParameter

class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "What my tool does"
    parameters = {
        "param1": ToolParameter(
            type="string",
            description="Parameter description"
        )
    }

    async def execute(self, param1: str) -> str:
        # Your tool logic here
        return f"Executed with {param1}"
```

Then enable it in `config/tools.yaml`:

```yaml
tools:
  my_tool:
    enabled: true
```

The tool will be auto-discovered and available to the LLM!

## Configuration

### Tools Configuration (`config/tools.yaml`)

Enable or disable tools without changing code:

```yaml
tools:
  get_time:
    enabled: true      # Always available (no hardware needed)

  toggle_led:
    enabled: false     # Enable when LED connected to GPIO

  check_motion:
    enabled: false     # Enable when PIR sensor connected
```

### Environment Variables (`.env`)

```bash
# Required
OPENROUTER_API_KEY=your_api_key_here

# Optional (defaults shown)
MODEL_NAME=anthropic/claude-3.5-sonnet

# Personalization - Give Pi-nocchio a soul!
USER_NAME=Friend                    # Your name (Pi-nocchio will know who it's assisting)
AGENT_NAME=Pi-nocchio               # Pi-nocchio's name (customize if you want)
AGENT_PERSONALITY=curious and playful  # Personality traits

# Logging
LOG_LEVEL=INFO                      # Options: DEBUG, INFO, WARNING, ERROR

# App metadata
APP_URL=https://github.com/hr23232323/pi-nocchio
```

**Personalization Example:**
```bash
USER_NAME=Harsh
AGENT_NAME=Woody
AGENT_PERSONALITY=witty and thoughtful
```

This gives Pi-nocchio a unique personality and makes interactions more personal!

### Logging / Debug Mode

Control how verbose the logs are:

```bash
LOG_LEVEL=INFO    # Clean output, hides HTTP request logs (default)
LOG_LEVEL=DEBUG   # Shows everything including HTTP requests to OpenRouter
LOG_LEVEL=WARNING # Only warnings and errors
LOG_LEVEL=ERROR   # Only errors
```

By default, noisy third-party logs (httpx, openai) are suppressed at INFO level and above. Set to DEBUG to see all HTTP traffic for troubleshooting.

## Current Tools

### `get_time`
Get the current date and time. No hardware required!

```
You: What time is it?
Pi-nocchio: The current time is 2026-01-05 19:30:45
```

### `wait`
Pause/sleep for a specified duration. The LLM can use this to create patterns and timing!

```
You: Blink the LED 3 times
   🔧 Using tool: toggle_led(led_name=status, state=on)
   🔧 Using tool: wait(seconds=0.5)
   🔧 Using tool: toggle_led(led_name=status, state=off)
   ... (repeats)

Pi-nocchio: Done! I blinked the status LED 3 times.
```

The LLM will creatively combine `wait` with other tools to create patterns, morse code, pulses, and more!

### `toggle_led`
Control an LED on/off via GPIO. Requires LED connected to a GPIO pin.

```
You: Turn on the status LED
   🔧 Using tool: toggle_led(led_name=status, state=on)

Pi-nocchio: ✅ LED 'status' is now ON
```

Configure your LED in `config/gpio_pins.yaml`:
```yaml
leds:
  status: 17      # GPIO pin number
```

### Emotion Expression Tools

**`express_emotion`** - Show emotions with colored LEDs
```
You: I'm excited to show you something!
   🔧 Using tool: express_emotion(emotion=excited)

Pi-nocchio: 🔴 Feeling excited! Red LED is glowing with energy!
```

Available emotions:
- `excited` (red LED) - Excitement, alerts, high energy
- `happy` (green LED) - Happiness, success, calm
- `curious` (yellow LED) - Thinking, wondering, processing
- `neutral` - All LEDs off

**`pulse_emotion`** - Breathing effect to show intensity of feeling

**`blink_emotion`** - Rapid blinks for bursts of emotion

### Audio Tools

**`play_tone`** - Play tones at specific frequencies through speaker
```
You: Play a 440 Hz tone
   🔧 Using tool: play_tone(frequency=440, duration=1.0)

Pi-nocchio: 🔊 Played 440 Hz tone for 1.0s
```

**`play_melody`** - Play musical melodies using note names
```
You: Play C E G C
   🔧 Using tool: play_melody(notes=['C4', 'E4', 'G4', 'C5'])

Pi-nocchio: 🎵 Played melody: C4, E4, G4, C5
```

**`beep_pattern`** - Custom beep patterns for alerts
```
You: Beep three times quickly
   🔧 Using tool: beep_pattern(pattern='short-short-short')

Pi-nocchio: 🔔 Played pattern: short-short-short
```

**`speak`** - Text-to-speech using Piper (local, offline, free!)
```
You: Say hello to me
   🔧 Using tool: speak(text='Hello! I'm Pi-nocchio, happy to meet you!')

Pi-nocchio: 🗣️ Spoke: "Hello! I'm Pi-nocchio, happy to meet you!"
```

Uses Piper - a fast neural TTS engine that runs locally on the Pi:
- ✅ **100% free** - no API costs
- ✅ **Offline** - works without internet
- ✅ **Fast** - optimized for Raspberry Pi
- ✅ **Natural voices** - high-quality neural TTS

Voice model is auto-downloaded by setup script!

Want a different voice? Download more from [Piper releases](https://github.com/rhasspy/piper/releases) and update `PIPER_VOICE` in `.env`

### `check_motion` (disabled by default)
Check motion sensor status. Requires PIR sensor connected via GPIO.

## Roadmap

### ✅ MVP (Complete)
- [x] Text-based CLI interface with colors
- [x] Simple agent loop with tool calling
- [x] Tool enable/disable via config
- [x] Personalized system prompt with configurable personality
- [x] Configurable logging levels
- [x] Example tool (GetTimeTool)
- [x] OpenRouter integration

### ✅ Iteration 2: GPIO Tools (Complete)
- [x] Add gpiozero dependency
- [x] Implement GPIO abstraction layer
- [x] Add functional LED control tool
- [x] Emotion expression LEDs (red, green, yellow)
- [x] Speaker/audio output tools (tones, melodies, beep patterns)
- [x] GPIO pin configuration via YAML
- [ ] Add functional PIR motion sensor tool (when hardware available)

### ✅ Iteration 3: Voice I/O (In Progress)
- [x] Text-to-speech using Piper (local, offline, free!)
- [ ] Speech-to-text (future: Vosk or Whisper for offline)
- [ ] Update agent loop for voice interaction
- [ ] Wake word detection

### Iteration 4: Vision
- [ ] Add picamera2 support
- [ ] Create camera abstraction
- [ ] Add vision tools for LLM

### Iteration 5+: Advanced Features
- [ ] Wake word detection
- [ ] Multi-agent coordination
- [ ] Web dashboard for monitoring
- [ ] Data logging and analytics

## Troubleshooting

### "Error loading configuration"
Make sure you have a `.env` file with your `OPENROUTER_API_KEY` set.

### "No tools are enabled"
Check `config/tools.yaml` and ensure at least one tool has `enabled: true`.

### "Piper not installed" or "Voice model not found" (for text-to-speech)
Re-run the setup script to install Piper and download voice models:
```bash
./scripts/setup-pi.sh
```

Or manually install:
```bash
uv sync  # Installs piper-tts
# Download voice model manually if needed
mkdir -p ~/.local/share/piper/voices
cd ~/.local/share/piper/voices
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json
```

### Dependencies not installing
Make sure you have `uv` installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Development

### Install dev dependencies

```bash
uv sync --all-extras
```

### Run linter

```bash
uv run ruff check src/
```

### Format code

```bash
uv run ruff format src/
```

## License

MIT

## Contributing

This is a "built in public" project! Contributions welcome. Feel free to:
- Add new tools
- Improve the agent loop
- Add documentation
- Report bugs

## About

Pi-nocchio is a playful exploration of giving LLMs a physical body. The name comes from Pinocchio's dream of becoming a real boy - our LLM dreams of becoming a real... robot? 🤖
