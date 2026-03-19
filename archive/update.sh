#!/bin/bash

install_ai_config() {
    CONFIG_PATH="$HOME/.termux-doctor-ai"

    echo "[AI] Checking for AI config..."

    if [ -f "$CONFIG_PATH" ]; then
        echo "[AI] Config already exists at $CONFIG_PATH"
        return
    fi

    echo "[AI] Installing AI config template..."

    cat <<EOF > "$CONFIG_PATH"
# Termux-Doctor AI Configuration
# Replace PUT_YOUR_HF_TOKEN_HERE with your HuggingFace token

HF_TOKEN="PUT_YOUR_HF_TOKEN_HERE"
EOF

    echo "[AI] AI config installed."
    echo "[AI] Edit $CONFIG_PATH and add your HuggingFace token."
}

# Run the installer
install_ai_config

