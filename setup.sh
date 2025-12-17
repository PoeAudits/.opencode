#!/bin/bash

# Set up opencode config from current directory
CONFIG_DIR="$HOME/.config/opencode"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Backup existing config if it exists
if [ -d "$CONFIG_DIR" ] && [ "$(ls -A "$CONFIG_DIR" 2>/dev/null)" ]; then
    echo "Backing up existing config to $CONFIG_DIR.backup.$(date +%s)"
    mv "$CONFIG_DIR" "$CONFIG_DIR.backup.$(date +%s)"
    mkdir -p "$CONFIG_DIR"
fi

# Copy all files from script directory to config location
cp -r "$SCRIPT_DIR"/* "$CONFIG_DIR/"

echo "Config installed to $CONFIG_DIR"