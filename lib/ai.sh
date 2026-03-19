#!/bin/bash

CONFIG_PATH="$HOME/.termux-doctor-ai"

if [ ! -f "$CONFIG_PATH" ]; then
    echo "[AI] No config file found at $CONFIG_PATH"
    exit 1
fi

source "$CONFIG_PATH"

if [ -z "$HF_TOKEN" ]; then
    echo "[AI] HF_TOKEN is missing in $CONFIG_PATH"
    exit 1
fi

MODEL="HuggingFaceH4/zephyr-7b-beta"

echo "[AI] Sending test request to HuggingFace Router..."
echo

curl -v \
    -X POST \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"inputs": "Say hello from Termux-Doctor."}' \
    https://router.huggingface.co/$MODEL \
    -o /tmp/ai_output.json

echo
echo "[AI] Raw Response:"
cat /tmp/ai_output.json 2>/dev/null || echo "[AI] No output file was created."
echo

