import os
import sys
import subprocess
from google import genai

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/gemini.key")
INSTALL_DIR = os.path.expanduser("~/.termux_doctor")

def print_banner():
    os.system('clear')
    print(f"{G}      .      .{Y}        _____________________________________________{RS}")
    print(f"{G}     / \    / \{Y}      |                                             |{RS}")
    print(f"{G}    /   \__/   \{Y}     |{G}               TERMUX-DOCTOR{Y}                 |{RS}")
    print(f"{G}    \   /  \   /{Y}     |{G}        > Network DNA Analysis v1.0 <{Y}        |{RS}")
    print(f"{G}     \_/    \_/{Y}      |_____________________________________________|{RS}")

def repair_system():
    print(f"{Y}[*] Starting Self-Healing Protocol...{RS}")
    try:
        # 1. Re-link Alias
        alias_file = os.path.expanduser("~/.termux_doctor_alias")
        with open(alias_file, 'w') as f:
            f.write(f"alias doctor='python {INSTALL_DIR}/core/main.py'\n")
        
        # 2. Strip Windows line endings from bashrc and alias
        os.system("sed -i 's/\\r//g' ~/.bashrc")
        os.system(f"sed -i 's/\\r//g' {alias_file}")
        
        # 3. Ensure bashrc sources the alias
        bashrc = os.path.expanduser("~/.bashrc")
        if "termux_doctor_alias" not in open(bashrc).read():
            with open(bashrc, 'a') as f:
                f.write("\nsource ~/.termux_doctor_alias\n")
        
        print(f"{G}✅ System Repaired. Restart Termux or type 'source ~/.bashrc'.{RS}")
    except Exception as e:
        print(f"{R}❌ Repair Failed: {e}{RS}")

def main():
    print_banner()
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                api_key = f.read().strip()

        user_input = input(f"\n{G}Dr. Prompt > {RS}").strip()
        
        if not user_input: continue
        if user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        # REPAIR COMMAND
        if user_input.lower() == 'repair system':
            repair_system()
            continue

        # KEY ROTATION
        if user_input.lower() == 'update key':
            new_val = input(f"{Y}🔑 Paste New Key:{RS} ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f:
                f.write(new_val)
            print(f"{G}✅ Key Saved.{RS}")
            continue

        if not api_key:
            print(f"{R}❌ No Key Found. Use 'update key'.{RS}")
            continue

        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            response = client.models.generate_content(model="gemini-1.5-flash", contents=user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.text}")
        except Exception as e:
            print(f"{R}❌ Handshake Error: {e}{RS}")

if __name__ == '__main__':
    main()