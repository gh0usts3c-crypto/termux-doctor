import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

def get_center(text):
    width = shutil.get_terminal_size().columns
    return text.center(width)

def print_banner():
    os.system('clear')
    width = shutil.get_terminal_size().columns
    helix = [" .   . ", "/ \ / \\", "\  X  /", " \/ \/ "]
    for line in helix: print(f"{G}{get_center(line)}{RS}")
    print(f"{Y}{get_center('_' * 30)}{RS}")
    print(f"{G}{get_center('TERMUX-DOCTOR v2.4')}{RS}")
    print(f"{G}{get_center('[ OPENROUTER ENGINE ]')}{RS}")
    print(f"{Y}{get_center('_' * 30)}{RS}")
    print(f"\n{Y}{get_center('Type \"help\" for the manual')}{RS}\n")

def show_help():
    print(f"\n{Y}📋 --- [ DOCTOR COMMAND MANUAL ] ---{RS}")
    print(f"{G}help{RS}          - Display this command list")
    print(f"{G}update key{RS}    - Paste your OpenRouter.ai API Key")
    print(f"{G}repair system{RS} - Fix terminal headers and API level")
    print(f"{G}exit / quit{RS}   - Close the clinic")
    print(f"{Y}--------------------------------------{RS}\n")

def main():
    print_banner()
    while True:
        # Load key dynamically
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input: continue
        
        cmd = user_input.lower()
        if cmd in ['exit', 'quit']: sys.exit(0)
        if cmd == 'help':
            show_help()
            continue
        if cmd == 'update key':
            val = input(f"{Y}🔑 Paste OpenRouter Key:{RS} ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print(f"{G}✅ Key Saved. Try a prompt now.{RS}")
            continue

        # API Logic (Only runs if not a command)
        if not api_key:
            print(f"{R}❌ No OpenRouter Key found.{RS}")
            print(f"{Y}💡 Get one at: https://openrouter.ai/keys{RS}")
            continue

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            response = client.chat.completions.create(
                model="google/gemini-flash-1.5", 
                messages=[{"role": "user", "content": user_input}]
            )
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
        except Exception as e:
            print(f"{R}❌ API Error: {e}{RS}")

if __name__ == '__main__':
    main()