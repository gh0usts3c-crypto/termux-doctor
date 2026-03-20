import os
import subprocess
import re

def run():
    print("\033[93m[*] Initiating Level-6 Regex Ping Sweep...\033[0m")
    
    try:
        # Step 1: Get raw output from the system
        raw_output = subprocess.check_output("ip -o -4 addr show wlan0", shell=True).decode()
        
        # Step 2: Extract CIDR using Regex (e.g., 192.168.1.5/24)
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})', raw_output)
        
        if match:
            target = match.group(1)
            print(f"\033[92m[+] [L6-SUCCESS] Subnet Identified: {target}\033[0m")
            print("\033[93m[*] Scanning for active hosts... (Polite Mode)\033[0m")
            # -sn: Ping Scan, -PE: ICMP Echo, -T3: Normal Speed
            os.system(f"nmap -sn -PE {target}")
            print("\033[92m✅ Sweep Complete.\033[0m")
        else:
            # Emergency Fallback if Regex fails to find wlan0
            print("\033[93m[!] wlan0 unreadable. Attempting standard Class-C scan...\033[0m")
            os.system("nmap -sn -PE 192.168.1.0/24 192.168.0.0/24")
            
    except Exception as e:
        print(f"\033[91m❌ Sweep Error: {e}\033[0m")