import os
import sys
import shutil
from google import genai

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/gemini.key")

# The 'Failover' list - will try these in order
MODELS = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]

def main():
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input or user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        if user_input.lower() == 'update key':
            val = input(f"🔑 New Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            continue

        try:
            client = genai.Client(api_key=api_key)
            success = False
            
            for model_id in MODELS:
                try:
                    res = client.models.generate_content(model=model_id, contents=user_input)
                    print(f"\n{Y}👨‍⚕️ [Doctor ({model_id})]:{RS}\n{res.text}\n")
                    success = True
                    break
                except Exception:
                    continue
            
            if not success:
                print(f"{R}❌ 404/API Error: No compatible models found for this key.{RS}")
                print(f"{Y}💡 Tip: Ensure 'Generative Language API' is enabled in Cloud Console.{RS}")
                
        except Exception as e:
            print(f"{R}❌ SYSTEM ERROR: {e}{RS}")

if __name__ == '__main__':
    main()