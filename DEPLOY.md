# Deploying Pi-nocchio to Raspberry Pi

Quick guide to get Pi-nocchio running on your Raspberry Pi.

## Prerequisites

- Raspberry Pi with Raspberry Pi OS installed
- Internet connection
- SSH access (or direct terminal access)

## Quick Start (5 minutes)

### 1. SSH into your Pi

```bash
ssh pi@raspberrypi.local
# OR use your Pi's IP address
ssh pi@192.168.1.100
```

### 2. Clone the repository

```bash
cd ~
git clone https://github.com/hr23232323/pi-nocchio.git
cd pi-nocchio
```

### 3. Run the setup script

```bash
chmod +x scripts/setup-pi.sh
./scripts/setup-pi.sh
```

This will:
- Update system packages
- Install uv package manager
- Install Python dependencies
- Create a `.env` template

### 4. Add your OpenRouter API key

```bash
nano .env
```

Add your API key:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
MODEL_NAME=anthropic/claude-3.5-sonnet
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### 5. Run Pi-nocchio!

```bash
./scripts/run.sh
```

Or:

```bash
uv run python -m pinocchio
```

## Manual Setup (if you prefer)

If you want to do it manually instead of using the setup script:

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# 3. Clone repo
git clone https://github.com/hr23232323/pi-nocchio.git
cd pi-nocchio

# 4. Install dependencies
uv sync

# 5. Configure
cp .env.example .env
nano .env  # Add your API key

# 6. Run
uv run python -m pinocchio
```

## Running on Boot (Optional)

To make Pi-nocchio start automatically when your Pi boots up:

### Create a systemd service

```bash
sudo nano /etc/systemd/system/pinocchio.service
```

Add:
```ini
[Unit]
Description=Pi-nocchio Agent
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pi-nocchio
ExecStart=/home/pi/.cargo/bin/uv run python -m pinocchio
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pinocchio.service
sudo systemctl start pinocchio.service
```

Check status:
```bash
sudo systemctl status pinocchio.service
```

View logs:
```bash
sudo journalctl -u pinocchio.service -f
```

## Testing

Once running, you should see:
```
Pi-nocchio is ready! (Type 'quit' to exit)

You:
```

Try:
```
You: What time is it?
[Using tool: get_time with args: {}]

Pi-nocchio: The current time is 2026-01-05 20:15:30
```

## Troubleshooting

### "uv: command not found"
The uv installation didn't add to PATH. Run:
```bash
source $HOME/.cargo/env
```

Or add to your `.bashrc`:
```bash
echo 'source $HOME/.cargo/env' >> ~/.bashrc
source ~/.bashrc
```

### "Error loading configuration"
Make sure your `.env` file exists and has the API key:
```bash
cat .env  # Should show your OPENROUTER_API_KEY
```

### Permission denied on scripts
Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Can't connect to OpenRouter
Check internet connection:
```bash
ping -c 3 openrouter.ai
```

## Next Steps

- Enable GPIO tools in `config/tools.yaml` when you connect hardware
- Add voice I/O (coming in Iteration 3)
- Connect sensors and actuators
- Make it a real boy! 🤖
