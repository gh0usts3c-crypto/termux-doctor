import os
import subprocess

def run():
    print("\033[93m[*] Initializing Robust Network Discovery...\033[0m")
    
    # 2026 Termux-Safe IP Discovery
    try:
        # Step 1: Identify the active WLAN interface and its CIDR
        cmd = "ip -o -4 addr show wlan0 | awk '{print }'"
        target = subprocess.check_output(cmd, shell=True).decode().strip()
        
        if not target:
            print("\033[93m[!] wlan0 not found. Attempting universal search...\033[0m")
            # Fallback: Find the first non-loopback inet address
            cmd = "ip -o -4 addr | grep -v '127.0.0.1' | head -n 1 | awk '{print }'"
            target = subprocess.check_output(cmd, shell=True).decode().strip()

        if target:
            print(f"\033[92m[+] Network Identified: {target}\033[0m")
            print("\033[93m[*] Running Host Discovery (Ping Scan)...\033[0m")
            os.system(f"nmap -sn {target}")
            print(f"\033[92m✅ Discovery Complete.\033[0m")
        else:
            print("\033[91m❌ Error: Could not resolve local subnet.\033[0m")
            print("💡 Check if WiFi is enabled or try 'pkg install nmap'.")
            
    except Exception as e:
        print(f"\033[91m❌ Plugin Error: {e}\033[0m")