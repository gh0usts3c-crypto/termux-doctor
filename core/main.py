import sys, subprocess, os

class DrTools:
    def __init__(self, ai_enabled=False):
        self.debug_log = []
        self.ai_enabled = ai_enabled
        self.version = "3.5-GOLD"
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

def main():
    ai_status = "--ai" in sys.argv
    tools = DrTools(ai_enabled=ai_status)
    
    os.system('clear')
    print("\033[92m" + "="*45)
    print(f"  TERMUX-DOCTOR v{tools.version} | GHOST-PROTOCOL")
    print("="*45 + "\033[0m")
    
    if tools.ai_enabled: print("\033[93m[!] AI Engine: AWAKE\033[0m")
    else: print("\033[90m[i] AI Engine: DORMANT (Use 'doctor --ai' to wake)\033[0m")
    
    # DYNAMIC COMMAND MAP
    while True:
        try:
            cmd = input("\n\033[92mdoctor > \033[0m").strip().lower()
            if cmd in ["exit", "quit"]: break
            
            # THE MANUAL / HELP COMMAND
            if cmd in ["?", "help", "man"]:
                print("\n\033[93mAVAILABLE COMMANDS:\033[0m")
                print("  'device id' : Run Ghost-ID Network Scanner")
                print("  'exit'      : Terminate Ghost-Protocol")
                print("  '?'         : Show this Manual")
                
            elif cmd == "device id":
                p_path = os.path.join(tools.base_path, "plugins", "plugin_device_id.py")
                if os.path.exists(p_path):
                    # Forcing a fresh read to avoid cache desync
                    with open(p_path, "r") as f:
                        code = f.read()
                    exec(code, {'tools': tools})
                else:
                    print(f"\033[91m[!] Error: Plugin not found at {p_path}\033[0m")
            
            else:
                if cmd: print(f"\033[90m[i] Unknown command: '{cmd}'. Type '?' for help.\033[0m")
                
        except KeyboardInterrupt: break
        except Exception as e: print(f"\033[91m[!] Error: {e}\033[0m")

if __name__ == "__main__":
    main()