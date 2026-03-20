import os
def run():
    print("\033[93m[*] Executing Local Net Audit...\033[0m")
    # Using 'ip -c addr' for colorized Termux output
    os.system("ip -c addr")
    print("\033[92m✅ Local interface check complete.\033[0m")