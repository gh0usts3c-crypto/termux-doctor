import sys, subprocess, os, glob

class DrTools:
    def __init__(self, ai_enabled=False):
        self.debug_log = []
        self.ai_enabled = ai_enabled
        self.version = "3.6-TITAN"
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
    print("\033[92m" + "="*45 + "\n  TERMUX-DOCTOR v" + tools.version + " | GHOST-PROTOCOL\n" + "="*45 + "\033[0m")
    
    while True:
        try:
            cmd = input("\n\033[92mdoctor > \033[0m").strip().lower()
            if cmd in ["exit", "quit"]: break
            
            # THE TITAN MANUAL (Full List)
            if cmd in ["?", "help", "man"]:
                print("\n\033[93m--- FULL COMMAND MANUAL ---\033[0m")
                print("  'device id'    : Run Ghost-ID Network Scanner")
                print("  'sniffer'      : (PENDING) Traffic Analysis")
                print("  'net guard'    : (PENDING) Intrusion Alert System")
                print("  'sys diag'     : Termux System Health Check")
                print("  'ghost wipe'   : Clear all Logs and History")
                print("  'exit'         : Securely Terminate")
                
            elif cmd == "device id":
                p_path = os.path.join(tools.base_path, "plugins", "plugin_device_id.py")
                if os.path.exists(p_path):
                    with open(p_path, "r") as f: exec(f.read(), {'tools': tools})
                else: print("\033[91m[!] Plugin Missing.\033[0m")
            
            # ADD FUTURE COMMAND HOOKS HERE
            elif cmd in ["sniffer", "net guard", "sys diag", "ghost wipe"]:
                print(f"\033[93m[!] Module '{cmd}' is currently being reconstructed for v3.6.\033[0m")
                
            else:
                if cmd: print(f"\033[90m[i] Unknown: '{cmd}'. Type '?' for full list.\033[0m")
                
        except KeyboardInterrupt: break
        except Exception as e: print(f"\033[91m[!] Error: {e}\033[0m")

if __name__ == "__main__":
    main()