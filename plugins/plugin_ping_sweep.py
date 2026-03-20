import os
import subprocess
import re

def run():
    print("\033[93m[*] Initiating User-Mode Multi-Port Discovery...\033[0m")
    
    try:
        # Step 1: Extract CIDR Subnet via Regex (Bypasses '23' error)
        raw_output = subprocess.check_output("ip -o -4 addr show wlan0", shell=True).decode()
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})', raw_output)
        
        if match:
            target = match.group(1)
            print(f"\033[92m[+] Network Identified: {target}\033[0m")
            print("\033[94m[*] Probing Stealth Ports (80, 443, 22, 445, 8080)...\033[0m")
            
            # -sn: Skip heavy port scan (Discovery Only)
            # -PS: TCP SYN discovery (Bypasses Root requirement)
            # --open: Only show hosts that actually respond
            os.system(f"nmap -sn -PS80,443,22,445,8080 --max-retries 1 {target}")
            
            print("\033[92m✅ Discovery Complete.\033[0m")
        else:
            print("\033[91m❌ Error: Subnet could not be mapped via wlan0.\033[0m")
            
    except Exception as e:
        print(f"\033[91m❌ Sweep Error: {e}\033[0m")