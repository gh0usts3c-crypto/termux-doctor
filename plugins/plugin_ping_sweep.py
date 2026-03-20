import os
import subprocess

def run():
    print("\033[93m[*] Initiating Level-6 Ping Sweep (ICMP Broadcast)...\033[0m")
    try:
        # Identify the local subnet automatically
        cmd = "ip -o -4 addr show wlan0 | awk '{print }'"
        target = subprocess.check_output(cmd, shell=True).decode().strip()
        
        if not target:
            target = "192.168.1.0/24" # Default fallback
            
        print(f"\033[94m[*] Sweeping Subnet: {target}\033[0m")
        # -sn: Ping Scan, -PE: ICMP Echo, --min-parallelism: Speed up
        os.system(f"nmap -sn -PE --min-parallelism 100 {target}")
        print("\033[92m✅ Sweep Complete. Use these IPs for 'silent id'.\033[0m")
    except Exception as e:
        print(f"\033[91m❌ Sweep Failed: {e}\033[0m")