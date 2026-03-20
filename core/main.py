import os, sys, re, subprocess, importlib.util
from openai import OpenAI

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
    DrTools.run_cmd("command -v nmap || pkg install nmap -y", silent=True)
    DrTools.run_cmd("command -v nc || pkg install netcat-openbsd -y", silent=True)

def print_banner(ai_status):
    os.system('clear')
    status = f"{G}ONLINE{RS}" if ai_status else f"{R}STEALTH{RS}"
    print(f"{G} .   .   {Y}=========================={RS}")
    print(f"{G}/ \ / \  {Y} TERMUX-DOCTOR v3.8.1{RS}")
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

        if cmd == 'exit': sys.exit(0)
        if cmd in ['ai on', 'ai off']:
            ai_enabled = (cmd == 'ai on')
            print_banner(ai_enabled); continue
        
        if cmd == '?':
            print(f"{Y}--- SYSTEM COMMANDS ---{RS}")
            print(f"{G}ai on/off{RS}  - Toggle Cloud AI connectivity")
            print(f"{G}clear{RS}      - Wipe terminal and reset UI")
            print(f"{G}exit{RS}       - Terminate Doctor session")
            
            print(f"\n{Y}--- LOADED MODULES ---{RS}")
            for f in os.listdir(PLUGIN_DIR):
                if f.startswith('plugin_') and f.endswith('.py'):
                    name = f[7:-3].replace('_', ' ')
                    # Dynamic Doc Extraction
                    spec = importlib.util.spec_from_file_location("doc_mod", os.path.join(PLUGIN_DIR, f))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    doc = getattr(mod, 'DOC', 'External plugin module')
                    print(f"{G}{name:<12}{RS} - {doc}")
            print("")
            continue

        plugin_file = f"plugin_{cmd.replace(' ', '_')}.py"
        plugin_path = os.path.join(PLUGIN_DIR, plugin_file)
        if os.path.exists(plugin_path):
            spec = importlib.util.spec_from_file_location("mod", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.run(DrTools)
            continue

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