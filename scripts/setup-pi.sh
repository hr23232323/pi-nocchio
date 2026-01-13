#!/bin/bash
set -e

echo "========================================="
echo "   Pi-nocchio Raspberry Pi Setup"
echo "========================================="
echo ""

# Check if running on Linux (Raspberry Pi OS)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Warning: This script is designed for Raspberry Pi OS (Linux)"
    echo "   But we'll try to continue anyway..."
    echo ""
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt install -y \
    git \
    curl \
    python3-pip \
    python3-venv \
    swig \
    python3-dev \
    build-essential \
    liblgpio-dev \
    wget \
    unzip \
    portaudio19-dev

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add to current session
    export PATH="$HOME/.cargo/bin:$PATH"

    # Add to .bashrc if not already there
    if ! grep -q "cargo/bin" ~/.bashrc; then
        echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
    fi
else
    echo "✓ uv already installed"
fi

# Verify uv is accessible
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv installation completed but not in PATH"
    echo "   Run: source ~/.bashrc"
    echo "   Or:  source \$HOME/.cargo/env"
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
uv sync

# Download Piper voice model
echo "🎤 Setting up Piper TTS voice model..."
VOICE_NAME="en_US-lessac-medium"
VOICE_DIR="$HOME/.local/share/piper/voices"
VOICE_FILE="$VOICE_DIR/$VOICE_NAME.onnx"
VOICE_CONFIG="$VOICE_DIR/$VOICE_NAME.onnx.json"

if [ ! -f "$VOICE_FILE" ] || [ ! -f "$VOICE_CONFIG" ]; then
    echo "📥 Downloading Piper voice model ($VOICE_NAME) from Hugging Face..."
    mkdir -p "$VOICE_DIR"

    # Download voice model files from Hugging Face
    MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
    CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"

    wget -q --show-progress -O "$VOICE_FILE" "$MODEL_URL"
    wget -q --show-progress -O "$VOICE_CONFIG" "$CONFIG_URL"

    echo "✓ Voice model downloaded to $VOICE_DIR"
else
    echo "✓ Piper voice model already exists"
fi

# Download Vosk speech recognition model
echo "🎤 Setting up Vosk STT model..."
VOSK_MODEL_NAME="vosk-model-small-en-us-0.15"
VOSK_DIR="$HOME/.local/share/vosk/models"
VOSK_MODEL_DIR="$VOSK_DIR/$VOSK_MODEL_NAME"

if [ ! -d "$VOSK_MODEL_DIR" ]; then
    echo "📥 Downloading Vosk model ($VOSK_MODEL_NAME) from alphacephei.com..."
    mkdir -p "$VOSK_DIR"

    # Download and extract Vosk model
    VOSK_URL="https://alphacephei.com/vosk/models/$VOSK_MODEL_NAME.zip"
    TEMP_ZIP="/tmp/$VOSK_MODEL_NAME.zip"

    wget -q --show-progress -O "$TEMP_ZIP" "$VOSK_URL"
    unzip -q "$TEMP_ZIP" -d "$VOSK_DIR"
    rm "$TEMP_ZIP"

    echo "✓ Vosk model downloaded and extracted to $VOSK_MODEL_DIR"
else
    echo "✓ Vosk model already exists"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: You need to add your OpenRouter API key!"
    echo "   Edit .env and add your key:"
    echo "   nano .env"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Make run script executable
chmod +x scripts/run.sh

echo ""
echo "========================================="
echo "   ✅ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Add your OpenRouter API key to .env:"
echo "   nano .env"
echo ""
echo "2. Run Pi-nocchio:"
echo "   ./scripts/run.sh"
echo ""
echo "Or:"
echo "   uv run python -m pinocchio"
echo ""
echo "Happy hacking! 🤖"
