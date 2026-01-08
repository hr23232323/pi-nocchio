#!/bin/bash
set -e

echo "========================================="
echo "   Enabling PWM Audio on GPIO 18"
echo "========================================="
echo ""

# Check if running on Raspberry Pi
if [[ ! -f /boot/firmware/config.txt ]] && [[ ! -f /boot/config.txt ]]; then
    echo "⚠️  Warning: This doesn't look like a Raspberry Pi"
    echo "   /boot/firmware/config.txt or /boot/config.txt not found"
    exit 1
fi

# Determine config file location (varies by Pi OS version)
if [[ -f /boot/firmware/config.txt ]]; then
    CONFIG_FILE="/boot/firmware/config.txt"
else
    CONFIG_FILE="/boot/config.txt"
fi

echo "Using config file: $CONFIG_FILE"
echo ""

# Backup config file
echo "📝 Backing up config file..."
sudo cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
echo "✓ Backup created"
echo ""

# Check if PWM audio is already enabled
if grep -q "dtoverlay=audremap,pins_18_19" "$CONFIG_FILE"; then
    echo "✓ PWM audio already enabled in config"
else
    echo "🔧 Enabling PWM audio on GPIO 18/19..."

    # Add PWM audio configuration
    echo "" | sudo tee -a "$CONFIG_FILE" > /dev/null
    echo "# PWM Audio on GPIO 18/19 for speaker module" | sudo tee -a "$CONFIG_FILE" > /dev/null
    echo "dtoverlay=audremap,pins_18_19" | sudo tee -a "$CONFIG_FILE" > /dev/null
    echo "dtparam=audio=on" | sudo tee -a "$CONFIG_FILE" > /dev/null

    echo "✓ PWM audio configuration added"
fi

echo ""
echo "========================================="
echo "   Configuration Complete!"
echo "========================================="
echo ""
echo "⚠️  REBOOT REQUIRED!"
echo ""
echo "After rebooting, run:"
echo "  sudo raspi-config"
echo ""
echo "Navigate to:"
echo "  System Options → Audio → Select 'bcm2835 Headphones'"
echo ""
echo "Or run this command:"
echo "  amixer cset numid=3 1"
echo ""
echo "Then test with:"
echo "  speaker-test -t wav -c 2"
echo ""
echo "Ready to reboot? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Rebooting now..."
    sudo reboot
else
    echo "Reboot cancelled. Run 'sudo reboot' when ready."
fi
