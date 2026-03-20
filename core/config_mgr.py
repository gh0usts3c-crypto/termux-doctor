import os, json

CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/config.json")

def load_api_key():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            try:
                data = json.load(f)
                return data.get("gemini_key")
            except:
                pass
    
    # First-run setup
    print("\n🔑 Gemini API Key not found.")
    key = input("Please enter your Gemini 1.5 API Key: ").strip()
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"gemini_key": key}, f)
    
    print("✅ Key saved locally.")
    return key
