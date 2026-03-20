import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

SYSTEM_PROMPT = (
    "Role: Senior Termux & Linux Security Expert. "
    "Style: Professional, concise, technical. No conversational filler. "
    "Output: Direct answers, minimal text, maximum code. "
)

def print_banner(ai_status):
    os.system('clear')
    status_text = f"{G}ON{RS}" if ai_status else f"{R}OFF (STEALTH){RS}"
    print(f"{G}{' TERMUX-DOCTOR v3.1 '.center(40, '=')}{RS}")
    print(f"{Y}{f'[ AI ENGINE: {status_text} ]'.center(40)}{RS}\n")

def main():
    ai_enabled = True
    print_banner(ai_enabled)
    
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        p_color, p_label = (G, "Dr. Prompt") if ai_enabled else (R, "[STEALTH]")
        user_input = input(f"{p_color}{p_label} > {RS}").strip()
        
        if not user_input: continue
        cmd = user_input.lower()

        if cmd in ['exit', 'quit']: sys.exit(0)
        if cmd == 'ai off': ai_enabled = False; print_banner(ai_enabled); continue
        if cmd == 'ai on': ai_enabled = True; print_banner(ai_enabled); continue
        if cmd == 'clear': print_banner(ai_enabled); continue
        if cmd == 'update key':
            val = input(f"🔑 Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print("✅ Key Saved.")
            continue

        if not ai_enabled:
            print(f"{Y}[STEALTH ECHO]:{RS} {user_input}\n")
            continue

        if not api_key:
            print(f"{R}❌ No Key found.{RS}")
            continue

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            print(f"{Y}[*] Handshaking...{RS}", end="\r")
            
            response = client.chat.completions.create(
                model="openrouter/free", 
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                timeout=25.0
            )

            # --- V3.1 ERROR TRAP ---
            if not response or not response.choices:
                print(f"{R}❌ Error: API returned an empty response.{RS}")
                print(f"{Y}💡 Fix: Check https://openrouter.ai/settings/privacy - Enable 'Data Retention/Training' for free models.{RS}")
                continue

            content = response.choices[0].message.content
            print(" " * 30, end="\r")
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{content}\n")

        except Exception as e:
            print(f"{R}❌ System Error: {e}{RS}")

if __name__ == '__main__':
    main()