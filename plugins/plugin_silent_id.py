import os
import subprocess
import re

def run():
    target = input("\033[93m[?] Enter Target IP to Identify: \033[0m").strip()
    if not target: return

    print(f"\033[93m[*] Attempting Passive Identification for {target}...\033[0m")
    
    # Technique 1: Check ARP Cache (Zero Noise - reads local memory)
    print("\033[94m[1/2] Checking Local ARP Cache (Passive)...\033[0m")
    os.system(f"ip neighbor show {target}")

    # Technique 2: Nmap Stealth RPC/Service Check (Minimal Noise)
    # -sV: Service version, -T2: Polite/Slow timing to avoid detection
    print("\033[94m[2/2] Running Stealth Service Probe (Low Noise)...\033[0m")
    os.system(f"nmap -sV -T2 -Pn --script=banner {target}")
    
    print("\033[92m✅ Silent Audit Complete.\033[0m")