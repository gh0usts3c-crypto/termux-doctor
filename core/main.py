import os
import sys
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")
SYSTEM_PROMPT = "Role: Senior Network Security Auditor. Focus: Nmap, Netcat, and Termux local networking. Concise, zero fluff."

def print_banner(ai_status):
    os.system('clear')
    status = f"{G}ON{RS}" if ai_status else f"{R}OFF{RS}"
    print(f"{G} .   .   {Y}=========================={RS}")
    print(f"{G}/ \ / \  {Y} TERMUX-DOCTOR v3.3{RS}")
    print(f"{G}\  X  /  {Y} MODE: NET-AUDIT | {status}{RS}")
    print(f"{G} \/ \/   {Y}=========================={RS}")
    print(f"{Y} Type '?' for the manual.{RS}\n")

def main():
    ai_enabled = True
    print_banner(ai_enabled)
    
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        p_label = f"{G}Net-Audit > {RS}" if ai_enabled else f"{R}[STEALTH] > {RS}"
        user_input = input(p_label).strip()
        if not user_input: continue
        
        cmd = user_input.lower()
        if cmd in ['exit', 'quit']: sys.exit(0)
        
        # --- NEW NETWORK MACROS ---
        if cmd == 'net-prep':
            print(f"{Y}[*] Hardening Network Toolkit...{RS}")
            os.system("pkg update -y && pkg install nmap iproute2 netcat -y")
            print(f"{G}✅ Network Tools Ready.{RS}")
            continue

        if cmd in ['?', 'doc-help']:
            print(f"\n{Y}--- NET-AUDIT MANUAL ---{RS}")
            print(f"{G}net-prep{RS}  - Install Nmap/Netcat suite")
            print(f"{G}ai off{RS}    - Stealth Mode (No Cloud)")
            print(f"{G}ai on{RS}     - AI Consulting (Online)")
            print(f"{G}save log{RS}  - Export scan results")
            print(f"{G}clear{RS}     - Reset Terminal UI\n")
            continue

        if cmd == 'clear': print_banner(ai_enabled); continue

        # AI Handshake Logic (Standard v3.2 Stable)
        if ai_enabled and api_key:
            try:
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
                response = client.chat.completions.create(
                    model="openrouter/free", 
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_input}]
                )
                print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
            except Exception as e: print(f"{R}❌ Error: {e}{RS}")
        elif not ai_enabled:
            print(f"{Y}[STEALTH]:{RS} {user_input}\n")

if __name__ == '__main__':
    main()