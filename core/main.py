import sys, subprocess, os

class DrTools:
    def __init__(self, ai_enabled=False):
        self.debug_log = []
        self.ai_enabled = ai_enabled
        self.version = "3.4.5-STABLE"

    def log_error(self, module, error):
        self.debug_log.append(f"[{module}] {error}")

    def show_report(self):
        print("\n\033[94m--- POST-OP DIAGNOSTIC SUMMARY ---\033[0m")
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
            if cmd == "device id":
                # Manual stable load
                path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins", "plugin_device_id.py")
                exec(open(path).read(), {'tools': tools})
            elif cmd == "?":
                print("Commands: 'device id', 'exit', '?'")
        except KeyboardInterrupt: break
        except Exception as e: print(f"\033[91m[!] Error: {e}\033[0m")

if __name__ == "__main__":
    main()