import os
import sys
import time
from google import genai
from google.genai import errors

# DNA Banner Colors
G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
RS = "\033[0m"

def print_banner():
    os.system('clear')
    print(f"""
{G}      .      .{Y}        _____________________________________________{RS}
{G}     / \    / \{Y}      |                                             |{RS}
{G}    /   \__/   \{Y}     |{G}               TERMUX-DOCTOR{Y}                 |{RS}
{G}    \   /  \   /{Y}     |{G}        > Network DNA Analysis v1.0 <{Y}        |{RS}
{G}     \_/    \_/{Y}      |_____________________________________________|{RS}
    """)

def get_api_key():
    config_path = os.path.expanduser("~/.config/termux_doctor/gemini.key")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return f.read().strip()
    return None

def main():
    print_banner()
    api_key = get_api_key()
    if not api_key:
        print(f"{R}❌ Key Missing.{RS}")
        sys.exit(1)
    
    client = genai.Client(api_key=api_key)
    
    # Fail-Safe Model List (Ranked Newest to Most Compatible)
    MODELS = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    
    print(f"{Y}[*] Establishing Secure Handshake...{RS}")
    
    active_model = None
    for model_name in MODELS:
        try:
            # Silent Test Pulse
            client.models.generate_content(model=model_name, contents="ping")
            active_model = model_name
            break
        except Exception as e:
            if "API key not valid" in str(e):
                continue # Try the next model
            else:
                print(f"{R}❌ Connection Error: {e}{RS}")
                sys.exit(1)

    if not active_model:
        print(f"{R}❌ 400 Error: API Key is rejected for all models.{RS}")
        print(f"{Y}💡 ACTION REQUIRED: Visit AI Studio and check if Billing/Region is blocked.{RS}")
        sys.exit(1)

    print(f"{G}✅ Handshake Successful: {active_model} is ONLINE.{RS}")
    
    while True:
        user_input = input(f"\n{G}Dr. Prompt > {RS}")
        if user_input.lower() in ['exit', 'quit']: break
        try:
            response = client.models.generate_content(model=active_model, contents=user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor's Insight]:{RS}\n{response.text}")
        except Exception as e:
            print(f"{R}❌ Error: {e}{RS}")

if __name__ == '__main__':
    main()
