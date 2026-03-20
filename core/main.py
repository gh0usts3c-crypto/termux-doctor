import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

def get_center(text):
    width = shutil.get_terminal_size().columns
    return text.center(width)

def print_banner(ai_status):
    os.system('clear')
    status_text = f"{G}ON{RS}" if ai_status else f"{R}OFF (STEALTH){RS}"
    print(f"{G}{get_center('TERMUX-DOCTOR v2.9')}{RS}")
    print(f"{Y}{get_center(f'[ AI ENGINE: {status_text} ]')}{RS}\n")

def main():
    ai_enabled = True # Default to ON
    print_banner(ai_enabled)
    
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        # Dynamic Prompt based on Privacy Mode
        p_color = G if ai_enabled else R
        p_label = "Dr. Prompt" if ai_enabled else "[STEALTH]"
        user_input = input(f"{p_color}{p_label} > {RS}").strip()
        
        if not user_input: continue
        cmd = user_input.lower()

        # --- SYSTEM COMMANDS ---
        if cmd in ['exit', 'quit']: sys.exit(0)
        
        if cmd == 'ai off':
            ai_enabled = False
            print_banner(ai_enabled)
            print(f"{R}🛡️ Stealth Mode Active. API Disconnected.{RS}")
            continue
            
        if cmd == 'ai on':
            ai_enabled = True
            print_banner(ai_enabled)
            print(f"{G}📡 AI Mode Active. Handshake Restored.{RS}")
            continue

        if cmd == 'help':
            print(f"\n{Y}--- PRIVACY COMMANDS ---{RS}")
            print(f"{G}ai off{RS}  - Disable API (Safe for sensitive data)")
            print(f"{G}ai on{RS}   - Enable AI (Consult the Doctor)")
            print(f"{G}clear{RS}   - Reset UI / Wipe screen")
            print(f"{G}update key{RS} - Set OpenRouter Key\n")
            continue

        if cmd == 'clear':
            print_banner(ai_enabled)
            continue

        # --- LOGIC GATE ---
        if not ai_enabled:
            print(f"{Y}[STEALTH ECHO]:{RS} {user_input}")
            print(f"{R}(Data stayed local. No API call made.){RS}")
            continue

        if not api_key:
            print(f"{R}❌ No Key found. Use 'update key'.{RS}")
            continue

        # --- API HANDSHAKE ---
        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            print(f"{Y}[*] Consulting...{RS}", end="\r")
            response = client.chat.completions.create(
                model="openrouter/free", 
                messages=[{"role": "user", "content": user_input}]
            )
            print(" " * 30, end="\r")
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
        except Exception as e:
            print(f"{R}❌ Error: {e}{RS}")

if __name__ == '__main__':
    main()