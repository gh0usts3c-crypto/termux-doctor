import os
def run():
    print("\033[93m[*] Hardening Environment... Installing Nmap and Net-Tools\033[0m")
    # This command runs the native Termux package manager
    os.system("pkg update -y && pkg install nmap iproute2 -y")
    print("\033[92m✅ Environment Ready. Nmap is now available.\033[0m")