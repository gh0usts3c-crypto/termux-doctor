import os
import subprocess

def run():
    print("\033[93m[*] Mapping Local Network Subnet...\033[0m")
    
    # Logic to find the local IP range automatically
    try:
        # Get the default gateway/ip range
        cmd = "ip route | grep default | awk '{print }' | cut -d. -f1-3"
        gw = subprocess.check_output(cmd, shell=True).decode().strip()
        target = f"{gw}.0/24"
        
        print(f"\033[92m[+] Targeting Subnet: {target}\033[0m")
        os.system(f"nmap -sn {target}")
        print(f"\033[92m✅ Network Map Complete.\033[0m")
    except Exception as e:
        print(f"\033[91m❌ Discovery Error: {e}\033[0m")
        print("💡 Ensure 'nmap' is installed (pkg install nmap).")