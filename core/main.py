import sys, subprocess, os, glob, importlib.util

class DrTools:
    def __init__(self, ai_enabled=False):
        self.debug_log = []
        self.ai_enabled = ai_enabled
        self.version = "3.7-AURORA"
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def log_error(self, module, error):
        self.debug_log.append(f"[{module}] {error}")

    def show_report(self):
        print("\n\033[94m--- DIAGNOSTIC SUMMARY ---\033[0m")
        if not self.debug_log:
            print("\033[92m[✓] All systems nominal.\033[0m")
        else:
            for entry in self.debug_log:
                print(f"\033[91m[!] {entry}\033[0m")
        self.debug_log = []

def get_plugins(tools):
    """Dynamically finds all plugins and their commands."""
    plugins_map = {}
    plugin_files = glob.glob(os.path.join(tools.base_path, "plugins", "plugin_*.py"))
    
    for p_file in plugin_files:
        try:
            # Extract command name from filename (e.g., plugin_device_id.py -> device id)
            name = os.path.basename(p_file).replace("plugin_", "").replace(".py", "").replace("_", " ")
            plugins_map[name] = p_file
        except Exception as e:
            tools.log_error("Loader", str(e))
    return plugins_map

def main():
    ai_status = "--ai" in sys.argv
    tools = DrTools(ai_enabled=ai_status)
    
    os.system('clear')
    print("\033[92m" + "="*45 + "\n  TERMUX-DOCTOR v" + tools.version + " | GHOST-PROTOCOL\n" + "="*45 + "\033[0m")
    
    while True:
        # Re-scan plugins folder every loop to allow live retro-integration
        commands = get_plugins(tools)
        
        try:
            cmd = input("\n\033[92mdoctor > \033[0m").strip().lower()
            if cmd in ["exit", "quit"]: break
            
            if cmd in ["?", "help", "man"]:
                print("\n\033[93m--- AUTO-INTEGRATED MODULES ---\033[0m")
                for c_name in sorted(commands.keys()):
                    print(f"  '{c_name}'")
                print("  'exit'")
                
            elif cmd in commands:
                p_path = commands[cmd]
                with open(p_path, "r") as f:
                    exec(f.read(), {'tools': tools})
            
            elif cmd:
                print(f"\033[90m[i] Unknown: '{cmd}'. (Found {len(commands)} active modules)\033[0m")
                
        except KeyboardInterrupt: break
        except Exception as e: print(f"\033[91m[!] Error: {e}\033[0m")

if __name__ == "__main__":
    main()