import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

# The 2026 Production Model IDs for OpenRouter
MODEL_LIST = [
    "google/gemini-flash-1.5", 
    "google/gemini-pro-1.5",
    "meta-llama/llama-3-8b-instruct:free", # High-speed free fallback
    "mistralai/mistral-7b-instruct:free"   # Stability fallback
]

def get_center(text):
    width = shutil.get_terminal_size().columns
    return text.center(width)

def main():
    os.system('clear')
    width = shutil.get_terminal_size().columns
    print(f"{G}{get_center('TERMUX-DOCTOR v2.5')}{RS}")
    print(f"{Y}{get_center('[ UNIVERSAL ENGINE ONLINE ]')}{RS}\n")

    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input: continue
        
        cmd = user_input.lower()
        if cmd in ['exit', 'quit']: sys.exit(0)
        if cmd == 'help':
            print(f"\n{Y}--- COMMANDS ---{RS}\nupdate key | repair system | exit\n")
            continue
        if cmd == 'update key':
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
                print(f"\n{Y}👨‍⚕️ [Doctor ({model_id})]:{RS}\n{response.choices[0].message.content}\n")
                success = True
                break
            except Exception:
                continue # Try next model in list
        
        if not success:
            print(f"{R}❌ All endpoints failed. Check OpenRouter balance/key permissions.{RS}")

if __name__ == '__main__':
    main()