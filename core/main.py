import os
import sys
import importlib.util
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")
LOG_PATH = os.path.expanduser("~/doctor_session.log")

# DYNAMIC PATH RESOLUTION
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

SESSION_HISTORY = []

def get_plugins():
    if not os.path.exists(PLUGIN_DIR): return []
    return [f[7:-3].replace('_', ' ') for f in os.listdir(PLUGIN_DIR) if f.startswith('plugin_') and f.endswith('.py')]

def print_banner(ai_status):
    os.system('clear')
    status = f"{G}ONLINE{RS}" if ai_status else f"{R}STEALTH{RS}"
    print(f"{G} .   .   {Y}=========================={RS}")
    print(f"{G}/ \ / \  {Y} TERMUX-DOCTOR v3.4.2{RS}")
    print(f"{G}\  X  /  {Y} STATUS: {status}{RS}")
    print(f"{G} \/ \/   {Y}=========================={RS}")
    print(f"{Y} Type '?' for the complete manual.{RS}\n")

def main():
    ai_enabled = True
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
        
        if cmd == 'save log':
            with open(LOG_PATH, 'w') as f: f.write("\n".join(SESSION_HISTORY))
            print(f"{G}✅ Log Saved to {LOG_PATH}{RS}"); continue

        # --- REPAIRED MANUAL ('?') ---
        if cmd == '?':
            print(f"\n{Y}--- CORE COMMANDS ---{RS}")
            print(f"{G}ai on/off{RS}  - Toggle Cloud Connection")
            print(f"{G}save log{RS}   - Export session history")
            print(f"{G}clear{RS}      - Reset UI / Wipe Screen")
            print(f"{G}update key{RS} - Change OpenRouter API Key")
            
            plugins = get_plugins()
            if plugins:
                print(f"\n{Y}--- LOADED MODULES ---{RS}")
                for p in plugins: print(f"{G}{p}{RS}  - (External Plugin)")
            print("")
            continue

        # --- DYNAMIC PLUGIN EXECUTION ---
        plugin_file = f"plugin_{cmd.replace(' ', '_')}.py"
        plugin_path = os.path.join(PLUGIN_DIR, plugin_file)
        
        if os.path.exists(plugin_path):
            try:
                spec = importlib.util.spec_from_file_location("mod", plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.run()
                continue
            except Exception as e:
                print(f"{R}❌ Plugin Error: {e}{RS}"); continue

        # --- AI HANDSHAKE ---
        if ai_enabled and api_key:
            try:
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
                print(f"{Y}[*] Handshaking...{RS}", end="\r")
                response = client.chat.completions.create(
                    model="openrouter/free", 
                    messages=[{"role": "system", "content": "Professional Termux Guru Mode."}, {"role": "user", "content": user_input}]
                )
                print(" " * 30, end="\r")
                print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
                SESSION_HISTORY.append(f"USER: {user_input}\nAI: {response.choices[0].message.content}\n")
            except Exception as e: print(f"{R}❌ AI Error: {e}{RS}")
        elif not ai_enabled:
            print(f"{Y}[STEALTH]:{RS} {user_input}\n")

if __name__ == '__main__':
    main()