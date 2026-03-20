import os
import sys
from google import genai

# DNA Banner Colors
G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"

def print_banner():
    os.system('clear')
    print(f"{G}      .      .{Y}        _____________________________________________{RS}")
    print(f"{G}     / \    / \{Y}      |                                             |{RS}")
    print(f"{G}    /   \__/   \{Y}     |{G}               TERMUX-DOCTOR{Y}                 |{RS}")
    print(f"{G}    \   /  \   /{Y}     |{G}        > Network DNA Analysis v1.0 <{Y}        |{RS}")
    print(f"{G}     \_/    \_/{Y}      |_____________________________________________|{RS}")

def get_clean_key():
    path = os.path.expanduser("~/.config/termux_doctor/gemini.key")
    if not os.path.exists(path): return None
    with open(path, 'r') as f:
        # STRIP ALL: Newlines, spaces, and hidden Windows carriage returns
        return f.read().replace('\n', '').replace('\r', '').strip()

def main():
    print_banner()
    raw_key = get_clean_key()
    
    if not raw_key:
        print(f"{R}❌ Error: API Key not found in ~/.config/termux_doctor/gemini.key{RS}")
        return

    # Diagnostic: Show partial key to verify it loaded correctly
    print(f"{Y}[*] Loading Key: {raw_key[:4]}...{raw_key[-4:]}{RS}")

    try:
        client = genai.Client(api_key=raw_key)
        # 2026 Test Pulse (Downgraded to 1.5 for maximum compatibility)
        print(f"{Y}[*] Attempting Handshake with Gemini 1.5 Flash...{RS}")
        
        response = client.models.generate_content(model="gemini-1.5-flash", contents="Hi")
        print(f"{G}✅ Connection Established! Doctor is Online.{RS}")
        
        while True:
            cmd = input(f"\n{G}Dr. Prompt > {RS}")
            if cmd.lower() in ['exit', 'quit']: break
            res = client.models.generate_content(model="gemini-1.5-flash", contents=cmd)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.text}")
            
    except Exception as e:
        print(f"{R}❌ Handshake Failed: {e}{RS}")
        if "400" in str(e):
            print(f"{Y}💡 ANALYSIS: Your key was sent, but Google rejected it.{RS}")
            print(f"{Y}1. Check if the key in AI Studio matches: {raw_key[:4]}...{RS}")
            print(f"{Y}2. Ensure your Google Cloud Project has the 'Generative Language API' enabled.{RS}")

if __name__ == '__main__':
    main()