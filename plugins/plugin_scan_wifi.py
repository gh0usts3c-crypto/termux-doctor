import os
import subprocess
import re

def run():
    print("\033[93m[*] Initializing Regex-Hardened Discovery...\033[0m")
    
    try:
        # Step 1: Get the raw IP data from the system
        raw_output = subprocess.check_output("ip -o -4 addr show wlan0", shell=True).decode()
        
        # Step 2: Use Regex to find the CIDR (e.g., 192.168.1.5/24)
        # This looks for 4 groups of numbers separated by dots, followed by a slash and mask
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})', raw_output)
        
        if match:
            target = match.group(1)
            print(f"\033[92m[+] Regex Matched Subnet: {target}\033[0m")
            print("\033[93m[*] Running Nmap Host Discovery...\033[0m")
            os.system(f"nmap -sn {target}")
            print(f"\033[92m✅ Discovery Complete.\033[0m")
        else:
            print("\033[91m❌ Regex Fail: Could not extract IP from raw data.\033[0m")
            print(f"Raw Data received: {raw_output}")
            
    except Exception as e:
        # Final Fallback if wlan0 is protected/hidden
        print("\033[93m[!] wlan0 restricted. Trying Common Subnet Scan...\033[0m")
        os.system("nmap -sn 192.168.1.0/24 192.168.0.0/24")