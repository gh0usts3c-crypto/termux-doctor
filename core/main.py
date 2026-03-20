import os
import sys
import importlib.util
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

def auto_setup():
    print(f"{Y}[*] Level 6 Boot: Verifying System Dependencies...{RS}")
    # Silent check for nmap and netcat
    os.system("command -v nmap >/dev/null 2>&1 || pkg install nmap -y >/dev/null 2>&1")
    os.system("command -v nc >/dev/null 2>&1 || pkg install netcat-openbsd -y >/dev/null 2>&1")
    print(f"{G}[+] System Dependencies Verified.{RS}")

def get_plugins():
    if not os.path.exists(PLUGIN_DIR): os.makedirs(PLUGIN_DIR)
    return [f[7:-3].replace('_', ' ') for f in os.listdir(PLUGIN_DIR) if f.startswith('plugin_') and f.endswith('.py')]

def main():
    auto_setup()
    ai_enabled = True
    while True:
        # (Standard UI and Input Logic from v3.4.2)
        p_label = f"{G}Dr. Prompt > {RS}"
        user_input = input(p_label).strip()
        if not user_input: continue
        cmd = user_input.lower()

        # DYNAMIC PLUGIN LOADER
        plugin_file = f"plugin_{cmd.replace(' ', '_')}.py"
        plugin_path = os.path.join(PLUGIN_DIR, plugin_file)
        if os.path.exists(plugin_path):
            spec = importlib.util.spec_from_file_location("mod", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.run()
            continue
            
        # AI Fallback...
        print(f"{Y}👨‍⚕️ [Doctor]: Analyzing {user_input}...{RS}")

if __name__ == '__main__':
    main()