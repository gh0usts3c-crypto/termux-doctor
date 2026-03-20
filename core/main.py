import os
import sys
import time
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")
LOG_PATH = os.path.expanduser("~/doctor_session.log")

SESSION_HISTORY = []
SYSTEM_PROMPT = "Role: Senior Termux Engineer. Concisely provide technical commands. No fluff."

def print_banner(ai_status):
    os.system('clear')
    status = f"{G}ONLINE{RS}" if ai_status else f"{R}STEALTH{RS}"
    # Hard-coded layout for 2026 Termux stability
    print(f"{G} .   .   {Y}=========================={RS}")
    print(f"{G}/ \ / \  {Y} TERMUX-DOCTOR v3.2{RS}")
    print(f"{G}\  X  /  {Y} STATUS: {status}{RS}")
    print(f"{G} \/ \/   {Y}=========================={RS}")
    print(f"{Y} Type '?' for the manual.{RS}\n")

def main():
    ai_enabled = True
    print_banner(ai_enabled)
    
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        p_label = f"{G}Dr. Prompt > {RS}" if ai_enabled else f"{R}[STEALTH] > {RS}"
        user_input = input(p_label).strip()
        
        if not user_input: continue
        cmd = user_input.lower()

        # --- REFACTORED COMMANDS ---
        if cmd in ['exit', 'quit']: sys.exit(0)
        
        if cmd in ['?', 'doc-help']:
            print(f"\n{Y}--- MANUAL ---{RS}")
            print(f"{G}?{RS}         - Show this manual")
            print(f"{G}ai off{RS}    - Stealth Mode (No Cloud)")
            print(f"{G}ai on{RS}     - AI Mode (Online)")
            print(f"{G}save log{RS}  - Export session to ~/doctor_session.log")
            print(f"{G}clear{RS}     - Reset Terminal UI\n")
            continue

        if cmd == 'save log':
            with open(LOG_PATH, 'w') as f:
                f.write("\n".join(SESSION_HISTORY))
            print(f"{G}✅ Session saved to {LOG_PATH}{RS}")
            continue

        if cmd == 'ai off': ai_enabled = False; print_banner(ai_enabled); continue
        if cmd == 'ai on': ai_enabled = True; print_banner(ai_enabled); continue
        if cmd == 'clear': print_banner(ai_enabled); continue

        # --- LOGIC GATE ---
        if not ai_enabled:
            print(f"{Y}[STEALTH]:{RS} {user_input}\n")
            continue

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            print(f"{Y}[*] Handshaking...{RS}", end="\r")
            
            response = client.chat.completions.create(
                model="openrouter/free", 
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_input}]
            )
            
            answer = response.choices[0].message.content
            print(" " * 30, end="\r")
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{answer}\n")
            
            # Record for log
            SESSION_HISTORY.append(f"USER: {user_input}\nAI: {answer}\n")

        except Exception as e:
            print(f"{R}❌ Error: {e}{RS}")

if __name__ == '__main__':
    main()