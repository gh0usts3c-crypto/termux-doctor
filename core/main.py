import os
import sys
import shutil
from google import genai

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/gemini.key")

def get_center(text):
    width = shutil.get_terminal_size().columns
    return text.center(width)

def print_banner():
    os.system('clear')
    width = shutil.get_terminal_size().columns
    helix = [
        "      .      .      ",
        "     / \    / \     ",
        "    /   \__/   \    ",
        "    \   /  \   /    ",
        "     \_/    \_/     "
    ]
    
    for line in helix:
        print(f"{G}{get_center(line)}{RS}")
    
    border = "_" * min(width - 4, 50)
    print(f"{Y}{get_center(border)}{RS}")
    print(f"{G}{get_center('TERMUX-DOCTOR')}{RS}")
    print(f"{G}{get_center('> Network DNA Analysis v1.7 <')}{RS}")
    print(f"{Y}{get_center(border)}{RS}")
    print(f"\n{Y}{get_center('Type \"help\" for a list of commands')}{RS}\n")

def show_help():
    print(f"\n{Y}📋 --- [ DOCTOR COMMAND MANUAL ] ---{RS}")
    print(f"{G}help{RS}          - Display this command list")
    print(f"{G}update key{RS}    - Rotate or fix your Gemini API Key")
    print(f"{G}repair system{RS} - Fix terminal aliases and line endings")
    print(f"{G}exit / quit{RS}   - Safely close the clinic")
    print(f"{Y}--------------------------------------{RS}")
    print(f"Anything else you type is sent to the AI for diagnosis.\n")

def main():
    print_banner()
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input: continue
        
        # COMMAND INTERCEPTOR
        cmd = user_input.lower()
        if cmd in ['exit', 'quit']: 
            print(f"{Y}Closing session...{RS}")
            sys.exit(0)
            
        if cmd == 'help':
            show_help()
            continue

        if cmd == 'update key':
            val = input(f"{Y}🔑 Paste New API Key:{RS} ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print(f"{G}✅ Key Saved.{RS}")
            continue

        if cmd == 'repair system':
            print(f"{Y}[*] Repairing line endings...{RS}")
            os.system("sed -i 's/\\r//g' ~/.bashrc")
            print(f"{G}✅ System Sanitized.{RS}")
            continue

        # AI LOGIC
        if not api_key:
            print(f"{R}❌ No Key Found. Type 'update key' to begin.{RS}")
            continue

        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            res = client.models.generate_content(model="models/gemini-1.5-flash", contents=user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.text}\n")
        except Exception as e:
            print(f"{R}❌ ERROR: {e}{RS}")

if __name__ == '__main__':
    main()