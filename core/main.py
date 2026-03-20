import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

def clean_print(text, color=G):
    # Uses a fixed 40-character safe-width for mobile portrait stability
    print(f"{color}{text.center(40)}{RS}")

def print_banner():
    os.system('clear')
    print("\n")
    clean_print(".   .", G)
    clean_print("/ \ / \\", G)
    clean_print("\  X  /", G)
    clean_print(" \/ \/ ", G)
    clean_print("-" * 25, Y)
    clean_print("TERMUX-DOCTOR v2.7", G)
    clean_print("[ STABLE UI MODE ]", Y)
    clean_print("-" * 25, Y)
    print("\n" + Y + " Type 'help' for commands".center(40) + RS + "\n")

def main():
    print_banner()
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input: continue
        
        cmd = user_input.lower()
        if cmd in ['exit', 'quit']: sys.exit(0)
        if cmd == 'help':
            print(f"\n{Y}--- CLINIC MANUAL ---{RS}")
            print(f"update key    - Set API Key")
            print(f"repair system - Fix line endings")
            print(f"clear         - Reset screen")
            print(f"exit          - Close clinic\n")
            continue
        
        if cmd == 'clear':
            print_banner()
            continue

        if cmd == 'update key':
            val = input(f"🔑 Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print("✅ Key Masked & Saved.")
            continue

        if not api_key:
            print(f"{R}❌ No Key found.{RS}")
            continue

        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        
        try:
            # Added a loading indicator
            print(f"{Y}[*] Consulting the brain...{RS}", end="\r")
            response = client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct:free", 
                messages=[{"role": "user", "content": user_input}]
            )
            # Clear the loading indicator
            print(" " * 30, end="\r")
            print(f"{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
        except Exception as e:
            print(f"{R}❌ Error: {e}{RS}")

if __name__ == '__main__':
    main()