import os, json

CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/config.json")

def load_api_key():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f).get("gemini_key")
    
    key = input("🔑 New Setup: Enter Gemini 1.5 API Key: ").strip()
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"gemini_key": key}, f)
    return key
