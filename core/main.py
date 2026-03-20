import os
import sys
from google import genai

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/gemini.key")

def print_banner():
    os.system('clear')
    print(f"{G}      .      .{Y}        _____________________________________________{RS}")
    print(f"{G}     / \    / \{Y}      |                                             |{RS}")
    print(f"{G}    /   \__/   \{Y}     |{G}               TERMUX-DOCTOR{Y}                 |{RS}")
    print(f"{G}    \   /  \   /{Y}     |{G}        > Network DNA Analysis v1.0 <{Y}        |{RS}")
    print(f"{G}     \_/    \_/{Y}      |_____________________________________________|{RS}")

def repair_system():
    print(f"{Y}[*] Repairing System Links...{RS}")
    os.system("sed -i 's/\\r//g' ~/.bashrc")
    os.system("sed -i 's/\\r//g' ~/.termux_doctor/core/main.py")
    print(f"{G}✅ Repair Complete. Type 'source ~/.bashrc' if doctor alias fails.{RS}")

def main():
    print_banner()
    while True:
        # Load key dynamically so 'update key' works instantly
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                api_key = f.read().strip()

        user_input = input(f"\n{G}Dr. Prompt > {RS}").strip()
        if not user_input: continue
        if user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        if user_input.lower() == 'repair system':
            repair_system()
            continue

        if user_input.lower() == 'update key':
            val = input(f"{Y}🔑 Paste New API Key:{RS} ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print(f"{G}✅ Key Saved.{RS}")
            continue

        if not api_key:
            print(f"{R}❌ No Key Found. Type 'update key' to begin.{RS}")
            continue

        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            res = client.models.generate_content(model="gemini-1.5-flash", contents=user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.text}")
        except Exception as e:
            print(f"{R}❌ Handshake Failed: {e}{RS}")

if __name__ == '__main__':
    main()