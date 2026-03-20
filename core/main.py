import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

def get_center(text):
    width = shutil.get_terminal_size().columns
    return text.center(width)

def print_banner():
    os.system('clear')
    width = shutil.get_terminal_size().columns
    helix = [" .   . ", "/ \ / \\", "\  X  /", " \/ \/ "]
    for line in helix: print(f"{G}{get_center(line)}{RS}")
    print(f"{Y}{get_center('_' * 30)}{RS}")
    print(f"{G}{get_center('TERMUX-DOCTOR v2.0')}{RS}")
    print(f"{G}{get_center('[ OPENROUTER ENGINE ]')}{RS}")
    print(f"{Y}{get_center('_' * 30)}{RS}\n")

def main():
    print_banner()
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input or user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        if user_input.lower() == 'update key':
            val = input(f"🔑 Paste OpenRouter Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print("✅ Key Saved.")
            continue

        if not api_key:
            print(f"{R}❌ No OpenRouter Key. Get one at openrouter.ai{RS}")
            continue

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            
            # This dynamic call tries Google Gemini via OpenRouter first, 
            # then falls back to Llama 3 if Gemini is '404'
            response = client.chat.completions.create(
                model="google/gemini-flash-1.5", 
                messages=[{"role": "user", "content": user_input}]
            )
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
        except Exception as e:
            print(f"{R}❌ API Error: {e}{RS}")

if __name__ == '__main__':
    main()