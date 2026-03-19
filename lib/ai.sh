#!/data/data/com.termux/files/usr/bin/bash

ai_analyze() {
    local input_data="$1"

    # Load API key + endpoint
    source "$HOME/.termux-doctor-ai"

    if [ -z "$API_KEY" ]; then
        echo -e "\e[31m[ERROR]\e[0m No API key found in ~/.termux-doctor-ai"
        return 1
    fi

    # Send diagnostics to HuggingFace free model
    response=$(curl -s -X POST "$ENDPOINT" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"inputs\": \"Explain this: $input_data\"}")

    echo "$response"
}

