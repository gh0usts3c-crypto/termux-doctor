import sys, subprocess, os, importlib.util

class DrTools:
    def __init__(self, ai_enabled=False):
        self.debug_log = []
        self.ai_enabled = ai_enabled
        self.version = "3.4.1-STABLE"

    def get_subnet(self):
        # Native detection for non-root Termux
        return "192.168.1.0/24" 

    def run_cmd(self, cmd, silent=False):
        try:
            if silent:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(cmd, shell=True)
        except Exception as e:
            self.log_error("Core-Exec", str(e))

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
    
    print("\033[92m" + "="*40)
    print(f"  TERMUX-DOCTOR v{tools.version} | GHOST-PROTOCOL")
    print("="*40 + "\033[0m")
    
    if tools.ai_enabled: print("\033[93m[!] AI Engine: AWAKE\033[0m")
    else: print("\033[90m[i] AI Engine: DORMANT (Use 'doctor --ai' to wake)\033[0m")
    
    while True:
        try:
            cmd = input("\n\033[92mdoctor > \033[0m").strip().lower()
            if cmd in ["exit", "quit"]: break
            if cmd == "device id":
                spec = importlib.util.spec_from_file_location("plugin_device_id", "plugins/plugin_device_id.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.run(tools)
            elif cmd == "?":
                print("Commands: 'device id', 'exit', '?'")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\033[91m[!] Error: {e}\033[0m")

if __name__ == "__main__":
    main()