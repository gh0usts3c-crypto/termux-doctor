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
    print(f"[*] Repairing system line endings...")
    os.system("sed -i 's/\\r//g' ~/.bashrc")
    print(f"✅ Repair Complete.")

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
        
        if user_input.lower() == 'repair system':
            repair_system()
            continue

        if user_input.lower() == 'update key':
            val = input(f"🔑 Paste New API Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print(f"✅ Key Saved.")
            continue

        if not api_key:
            print(f"❌ No Key Found. Use 'update key'.")
            continue

        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            res = client.models.generate_content(model="gemini-1.5-flash", contents=user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.text}")
        except Exception as e:
            print(f"❌ Handshake Failed: {e}")

if __name__ == '__main__':
    main()