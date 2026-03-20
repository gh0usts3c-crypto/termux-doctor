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

def save_key(new_key):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    clean_key = new_key.replace('\n', '').replace('\r', '').strip()
    with open(CONFIG_PATH, 'w') as f:
        f.write(clean_key)
    return clean_key

def get_key():
    if not os.path.exists(CONFIG_PATH): return None
    with open(CONFIG_PATH, 'r') as f:
        return f.read().strip()

def main():
    print_banner()
    api_key = get_key()
    
    if not api_key:
        print(f"{Y}[!] No API Key stored. Please use 'update key' to add one.{RS}")
    
    while True:
        # We DON'T try to connect here anymore. We just wait for input.
        user_input = input(f"\n{G}Dr. Prompt > {RS}").strip()
        
        if not user_input: continue
        
        # 1. EMERGENCY ESCAPE
        if user_input.lower() in ['exit', 'quit']:
            print(f"{Y}👋 Closing the clinic...{RS}")
            sys.exit(0)
            
        # 2. KEY MANAGEMENT (Always accessible)
        if user_input.lower() == 'update key':
            print(f"{Y}🔑 Paste New API Key (or type 'cancel' to return):{RS}")
            new_val = input("> ").strip()
            if new_val.lower() != 'cancel':
                api_key = save_key(new_val)
                print(f"{G}✅ Key Saved.{RS}")
            continue

        # 3. AI DIAGNOSIS (Only tries when key is present)
        if not api_key:
            print(f"{R}❌ Error: You must 'update key' before diagnosing.{RS}")
            continue

        try:
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=user_input
            )
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.text}")
        except Exception as e:
            print(f"{R}❌ Handshake Failed: {e}{RS}")
            print(f"{Y}💡 Tip: Your key might be invalid. Type 'update key' to try another.{RS}")

if __name__ == '__main__':
    main()