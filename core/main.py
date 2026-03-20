import sys, subprocess, os

class DrTools:
    def __init__(self, ai_enabled=False):
        self.debug_log = []
        self.ai_enabled = ai_enabled
        self.version = "3.5-GOLD"
        # Force absolute pathing for plugins to prevent 'File Not Found' errors
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_subnet(self):
        return "192.168.1.0/24" 

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

def main():
    ai_status = "--ai" in sys.argv
    tools = DrTools(ai_enabled=ai_status)
    
    os.system('clear')
    print("\033[92m" + "="*45)
    print(f"  TERMUX-DOCTOR v{tools.version} | GHOST-PROTOCOL")
    print("="*45 + "\033[0m")
    
    if tools.ai_enabled: print("\033[93m[!] AI Engine: AWAKE\033[0m")
    else: print("\033[90m[i] AI Engine: DORMANT (Use 'doctor --ai' to wake)\033[0m")
    
    plugin_path = os.path.join(tools.base_path, "plugins", "plugin_device_id.py")

    while True:
        try:
            cmd = input("\n\033[92mdoctor > \033[0m").strip().lower()
            if cmd in ["exit", "quit"]: break
            if cmd == "device id":
                if os.path.exists(plugin_path):
                    exec(open(plugin_path).read(), {'tools': tools})
                else:
                    print(f"\033[91m[!] Error: Plugin not found at {plugin_path}\033[0m")
            elif cmd == "?":
                print("Commands: 'device id', 'exit', '?'")
        except KeyboardInterrupt: break
        except Exception as e: print(f"\033[91m[!] Error: {e}\033[0m")

if __name__ == "__main__":
    main()