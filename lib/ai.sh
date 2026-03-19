#!/bin/bash

CONFIG_PATH="$HOME/.termux-doctor-ai"

# Load token
if [ ! -f "$CONFIG_PATH" ]; then
    echo "[AI] No config file found at $CONFIG_PATH"
    exit 1
fi

source "$CONFIG_PATH"

if [ -z "$HF_TOKEN" ]; then
    echo "[AI] HF_TOKEN is missing in $CONFIG_PATH"
    exit 1
fi

MODEL="mistralai/Mistral-7B-Instruct-v0.2"

echo "[AI] Sending test request to HuggingFace..."

RESPONSE=$(curl -s \
    -X POST \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"inputs": "Say hello from Termux-Doctor."}' \
    https://api-inference.huggingface.co/models/$MODEL)

echo
echo "[AI] Response:"
echo "$RESPONSE"
echo

