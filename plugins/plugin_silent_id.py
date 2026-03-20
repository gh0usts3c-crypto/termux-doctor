import os
import subprocess
import re

def run():
    target = input("\033[93m[?] Target IP for Passive Audit: \033[0m").strip()
    if not target: return

    print(f"\033[93m[*] Initiating Ghost Discovery for {target}...\033[0m")
    
    try:
        # STEP 1: Layer-2 ARP Query (No ICMP/Ping)
        # --send-eth forces Layer-2 bypassing the OS IP stack
        cmd = f"nmap -sn -PR --send-eth {target}"
        output = subprocess.check_output(cmd, shell=True).decode()
        
        # Regex for MAC and Vendor
        mac_match = re.search(r"MAC Address: ([0-9A-F:]{17}) \((.*?)\)", output, re.IGNORECASE)
        
        if mac_match:
            print(f"\033[92m[+] [L2-SUCCESS] Identity: {mac_match.group(2)}\033[0m")
            print(f"\033[94m    Hardware ID: {mac_match.group(1)}\033[0m")
        else:
            print("\033[93m[!] Target is masked. Transitioning to TCP-ACK Discovery...\033[0m")
            # STEP 2: TCP ACK Scan (Does not open a connection)
            os.system(f"nmap -sn -PA {target}")

        # STEP 3: Passive Service Fingerprinting
        # -sV: Version, --version-intensity 0: Only read the initial banner (Very Quiet)
        print("\033[94m[*] Attempting Passive Banner Grab (Intensity 0)...\033[0m")
        os.system(f"nmap -sV --version-intensity 0 -T2 -Pn {target}")
        
    except Exception as e:
        print(f"\033[91m❌ Protocol Error: {e}\033[0m")

    print("\033[92m✅ Noiseless Audit Complete.\033[0m")