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
    python3-venv

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
