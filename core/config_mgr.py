import os

CONFIG_DIR = os.path.expanduser("~/.config/termux_doctor")
KEY_FILE = os.path.join(CONFIG_DIR, "gemini.key")

def load_api_key():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    else:
        print("\033[93m[!] No API Key found.\033[0m")
        key = input("🔑 Please enter your Gemini API Key: ")
        with open(KEY_FILE, "w") as f:
            f.write(key)
        return key
