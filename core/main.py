import os
import sys
from google import genai

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/gemini.key")

def main():
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"\n{G}Dr. Prompt > {RS}").strip()
        if not user_input or user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        if user_input.lower() == 'update key':
            val = input(f"🔑 New Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            continue

        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            # TRYING THE FULLY QUALIFIED PATH
            res = client.models.generate_content(model="models/gemini-1.5-flash", contents=user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.text}")
        except Exception as e:
            print(f"{R}❌ ERROR: {e}{RS}")

if __name__ == '__main__':
    main()