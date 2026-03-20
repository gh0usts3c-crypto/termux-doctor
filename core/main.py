import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

# UPDATED MARCH 2026 FREE ENDPOINTS
# openrouter/free is the 'Auto-Pilot' for free models
MODEL_LIST = [
    "openrouter/free",
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-7b-instruct-v0.1:free"
]

def main():
    os.system('clear')
    print(f"{G}TERMUX-DOCTOR v2.8{RS}")
    print(f"{Y}[ ENGINE: MARCH 2026 STABLE ]{RS}\n")

    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input or user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        if user_input.lower() == 'update key':
            val = input(f"🔑 Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print("✅ Key Saved.")
            continue

        if not api_key:
            print(f"{R}❌ No Key. Type 'update key'.{RS}")
            continue

        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        
        success = False
        print(f"{Y}[*] Establishing Handshake...{RS}", end="\r")
        
        for model_id in MODEL_LIST:
            try:
                response = client.chat.completions.create(
                    model=model_id, 
                    messages=[{"role": "user", "content": user_input}],
                    extra_headers={
                        "HTTP-Referer": "https://github.com/gh0usts3c-crypto",
                        "X-Title": "Termux-Doctor"
                    }
                )
                print(" " * 30, end="\r") # Clear the loading line
                print(f"\n{Y}👨‍⚕️ [Doctor ({model_id})]:{RS}\n{response.choices[0].message.content}\n")
                success = True
                break
            except Exception:
                continue
        
        if not success:
            print(f"\n{R}❌ All 2026 Free Endpoints Busy.{RS}")
            print(f"{Y}💡 Try again in 60s or check: https://openrouter.ai/activity{RS}")

if __name__ == '__main__':
    main()