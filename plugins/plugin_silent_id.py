import os
import subprocess

def run():
    target = input("\033[93m[?] Enter Target IP: \033[0m").strip()
    if not target: return

    print(f"\033[93m[*] Waking up neighbor table for {target}... (Low Noise)\033[0m")
    
    # Send 1 single ping to 'tickle' the ARP cache
    subprocess.run(["ping", "-c", "1", "-W", "1", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\033[94m[1/2] Extracting MAC/Vendor Data...\033[0m")
    # Grab the neighbor entry now that it's 'awake'
    neighbor = subprocess.check_output(f"ip neighbor show {target}", shell=True).decode().strip()
    
    if neighbor:
        print(f"\033[92m[+] Identity Found: {neighbor}\033[0m")
    else:
        print("\033[91m[!] Passive lookup failed. Device may be blocking ICMP.\033[0m")

    print("\033[94m[2/2] Running OS/Banner Fingerprint (Stealth Mode)...\033[0m")
    # -O: OS Detection, -sV: Service Detection, -T2: Polite
    os.system(f"nmap -sV -O -T2 -Pn --max-retries 1 {target}")
    
    print("\033[92m✅ Audit Complete.\033[0m")