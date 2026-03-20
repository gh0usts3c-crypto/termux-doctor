import os, sys, re, subprocess, importlib.util
from openai import OpenAI

# Global Styles
G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = os.path.join(BASE_DIR, "plugins")

class DrTools:
    @staticmethod
    def get_subnet():
        try:
            raw = subprocess.check_output("ip -o -4 addr show wlan0", shell=True).decode()
            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})', raw)
            return match.group(1) if match else "192.168.1.0/24"
        except: return "192.168.1.0/24"

    @staticmethod
    def run_cmd(cmd, silent=False):
        null = " >/dev/null 2>&1" if silent else ""
        os.system(f"{cmd}{null}")

def auto_setup():
    # Only installs if missing - 0% redundancy
    DrTools.run_cmd("command -v nmap || pkg install nmap -y", silent=True)
    DrTools.run_cmd("command -v nc || pkg install netcat-openbsd -y", silent=True)

def print_banner(ai_status):
    os.system('clear')
    status = f"{G}ONLINE{RS}" if ai_status else f"{R}STEALTH{RS}"
    print(f"{G} .   .   {Y}=========================={RS}")
    print(f"{G}/ \ / \  {Y} TERMUX-DOCTOR v3.8.0{RS}")
    print(f"{G}\  X  /  {Y} STATUS: {status}{RS}")
    print(f"{G} \/ \/   {Y}=========================={RS}\n")

def main():
    ai_enabled = True
    auto_setup()
    print_banner(ai_enabled)
    
    while True:
        p_label = f"{G}Dr. Prompt > {RS}" if ai_enabled else f"{R}[STEALTH] > {RS}"
        try:
            user_input = input(p_label).strip()
        except EOFError: break
        
        if not user_input: continue
        cmd = user_input.lower()

        # System Handlers
        if cmd == 'exit': sys.exit(0)
        if cmd in ['ai on', 'ai off']:
            ai_enabled = (cmd == 'ai on')
            print_banner(ai_enabled); continue
        
        if cmd == '?':
            print(f"{Y}--- SYSTEM ---{RS}\n{G}ai on/off | clear | exit{RS}")
            plugins = [f[7:-3].replace('_', ' ') for f in os.listdir(PLUGIN_DIR) if f.startswith('plugin_')]
            if plugins:
                print(f"\n{Y}--- MODULES ---{RS}")
                for p in plugins: print(f"{G}{p}{RS}")
            continue

        # Dynamic Plugin Execution
        plugin_file = f"plugin_{cmd.replace(' ', '_')}.py"
        plugin_path = os.path.join(PLUGIN_DIR, plugin_file)
        if os.path.exists(plugin_path):
            spec = importlib.util.spec_from_file_location("mod", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.run(DrTools) # Passing the toolset to the plugin
            continue

        # AI Logic (Simplified)
        if ai_enabled and os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: key = f.read().strip()
            try:
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
                print(f"{Y}[*] Consulting...{RS}", end="\r")
                res = client.chat.completions.create(model="openrouter/free", messages=[{"role":"user","content":user_input}])
                print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{res.choices[0].message.content}\n")
            except Exception as e: print(f"{R}❌ AI Error: {e}{RS}")

if __name__ == '__main__':
    main()