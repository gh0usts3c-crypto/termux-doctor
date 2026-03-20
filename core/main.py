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
    if not os.path.exists(CONFIG_PATH):
        print(f"{Y}🔑 [FIRST RUN] Please enter your Gemini API Key:{RS}")
        return save_key(input("> "))
    with open(CONFIG_PATH, 'r') as f:
        return f.read().strip()

def main():
    print_banner()
    api_key = get_key()
    
    while True:
        try:
            client = genai.Client(api_key=api_key)
            print(f"{G}🩺 Doctor Online (Key: {api_key[:4]}...{api_key[-4:]}){RS}")
            
            while True:
                user_input = input(f"\n{G}Dr. Prompt > {RS}").strip()
                
                if user_input.lower() in ['exit', 'quit']: sys.exit(0)
                
                # KEY ROTATION COMMAND
                if user_input.lower() == 'update key':
                    print(f"{Y}🔑 Enter New API Key (or type 'cancel'):{RS}")
                    new_val = input("> ").strip()
                    if new_val.lower() != 'cancel':
                        api_key = save_key(new_val)
                        print(f"{G}✅ Key Updated. Reconnecting...{RS}")
                        break # Break inner loop to re-init client
                    continue

                response = client.models.generate_content(model="gemini-1.5-flash", contents=user_input)
                print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.text}")
                
        except Exception as e:
            print(f"{R}❌ Error: {e}{RS}")
            api_key = save_key(input(f"{Y}Please enter a valid key to try again: {RS}"))

if __name__ == '__main__':
    main()