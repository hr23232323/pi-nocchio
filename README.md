# pi-nocchio

> The "I want to be a real boy" starter kit for LLMs built for Raspberry Pis

Give an LLM a physical body! Pi-nocchio is an autonomous agent system that runs on a Raspberry Pi, enabling LLMs to interact with the real world through sensors and actuators.

## Features

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
APP_URL=https://github.com/hr23232323/pi-nocchio
```

## Current Tools

### `get_time`
Get the current date and time. No hardware required!

```
You: What time is it?
Pi-nocchio: The current time is 2026-01-05 19:30:45
```

### `toggle_led` (disabled by default)
Control an LED on/off. Requires GPIO hardware to be connected.

### `check_motion` (disabled by default)
Check motion sensor status. Requires PIR sensor connected via GPIO.

## Roadmap

### MVP (Current)
- [x] Text-based CLI interface
- [x] Simple agent loop with tool calling
- [x] Tool enable/disable via config
- [x] Example tool (GetTimeTool)
- [x] OpenRouter integration

### Iteration 2: GPIO Tools
- [ ] Add gpiozero dependency
- [ ] Implement GPIO abstraction layer
- [ ] Add functional LED control tool
- [ ] Add functional PIR motion sensor tool

### Iteration 3: Voice I/O
- [ ] Add Vosk (speech-to-text)
- [ ] Add Piper (text-to-speech)
- [ ] Update agent loop for voice interaction
- [ ] Create setup script for model downloads

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
