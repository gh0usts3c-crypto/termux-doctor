import os
import sys
from google import genai

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"

def main():
    os.system('clear')
    print(f"{G}🩺 Doctor is checking in...{RS}")
    config_path = os.path.expanduser("~/.config/termux_doctor/gemini.key")
    
    if not os.path.exists(config_path):
        print(f"{R}❌ No Key Found.{RS}")
        return

    with open(config_path, 'r') as f:
        key = f.read().strip()

    client = genai.Client(api_key=key)
    try:
        # Fail-safe check
        response = client.models.generate_content(model="gemini-1.5-flash", contents="Test")
        print(f"{G}✅ Connection Established.{RS}")
        while True:
            cmd = input(f"\n{G}Dr. Prompt > {RS}")
            if cmd.lower() in ['exit', 'quit']: break
            res = client.models.generate_content(model="gemini-1.5-flash", contents=cmd)
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.text}")
    except Exception as e:
        print(f"{R}❌ Error: {e}{RS}")

if __name__ == '__main__':
    main()