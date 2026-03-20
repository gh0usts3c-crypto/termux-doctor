import os
import sys
import importlib.util
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

def auto_setup():
    # Silent check to prevent UI breakage
    os.system("command -v nmap >/dev/null 2>&1 || pkg install nmap -y >/dev/null 2>&1")
    os.system("command -v nc >/dev/null 2>&1 || pkg install netcat-openbsd -y >/dev/null 2>&1")

def get_plugins():
    if not os.path.exists(PLUGIN_DIR): os.makedirs(PLUGIN_DIR)
    return [f[7:-3].replace('_', ' ') for f in os.listdir(PLUGIN_DIR) if f.startswith('plugin_') and f.endswith('.py')]

def print_banner(ai_status):
    os.system('clear')
    status = f"{G}ONLINE{RS}" if ai_status else f"{R}STEALTH{RS}"
    print(f"{G} .   .   {Y}=========================={RS}")
    print(f"{G}/ \ / \  {Y} TERMUX-DOCTOR v3.7.1{RS}")
    print(f"{G}\  X  /  {Y} STATUS: {status}{RS}")
    print(f"{G} \/ \/   {Y}=========================={RS}")
    print(f"{Y} Type '?' for the manual.{RS}\n")

def main():
    ai_enabled = True
    auto_setup() # Run silently in background
    print_banner(ai_enabled)
    
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        p_label = f"{G}Dr. Prompt > {RS}" if ai_enabled else f"{R}[STEALTH] > {RS}"
        user_input = input(p_label).strip()
        if not user_input: continue
        
        cmd = user_input.lower()
        if cmd == 'exit': sys.exit(0)
        if cmd == 'ai off': ai_enabled = False; print_banner(ai_enabled); continue
        if cmd == 'ai on': ai_enabled = True; print_banner(ai_enabled); continue
        if cmd == 'clear': print_banner(ai_enabled); continue

        # --- MANUAL ---
        if cmd == '?':
            print(f"\n{Y}--- CORE COMMANDS ---{RS}")
            print(f"{G}ai on/off{RS} | {G}clear{RS} | {G}exit{RS}")
            plugins = get_plugins()
            if plugins:
                print(f"\n{Y}--- MODULES ---{RS}")
                for p in plugins: print(f"{G}{p}{RS}")
            print("")
            continue

        # --- PLUGIN EXECUTION ---
        plugin_file = f"plugin_{cmd.replace(' ', '_')}.py"
        plugin_path = os.path.join(PLUGIN_DIR, plugin_file)
        if os.path.exists(plugin_path):
            try:
                spec = importlib.util.spec_from_file_location("mod", plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.run()
                continue
            except Exception as e: print(f"{R}❌ Plugin Error: {e}{RS}"); continue

        # --- AI FALLBACK ---
        if ai_enabled and api_key:
            try:
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
                print(f"{Y}[*] Consulting...{RS}", end="\r")
                response = client.chat.completions.create(
                    model="openrouter/free", 
                    messages=[{"role": "system", "content": "Professional Security Guru."}, {"role": "user", "content": user_input}]
                )
                print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
            except Exception as e: print(f"{R}❌ AI Error: {e}{RS}")

if __name__ == '__main__':
    main()