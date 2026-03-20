import socket
import os
import subprocess

def run():
    target = input("\033[93m[?] Target IP for Socket-Level Audit: \033[0m").strip()
    if not target: return

    # List of 'Silent' ports to check for a handshake
    ports = [80, 443, 22, 135, 445, 8080]
    found = False

    print(f"\033[93m[*] Probing Socket Handshake (No-Scan Mode)...\033[0m")
    
    for port in ports:
        # Create a raw stream socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Fast timeout for stealth
        
        result = sock.connect_ex((target, port))
        
        if result == 0: # 0 means the port is OPEN and device is ALIVE
            print(f"\033[92m[+] [HANDSHAKE-SUCCESS] Device is ACTIVE on Port {port}\033[0m")
            found = True
            sock.close()
            break
        sock.close()

    if found:
        print("\033[94m[*] Device confirmed. Pulling MAC from Kernel ARP Table...\033[0m")
        # Now that a socket was opened, the kernel MUST have the MAC in 'ip neigh'
        try:
            neigh = subprocess.check_output(f"ip neigh show {target}", shell=True).decode().strip()
            if neigh:
                print(f"\033[92m[+] Identity Found: {neigh}\033[0m")
            else:
                print("\033[93m[!] Kernel hidden. Running low-intensity Nmap fallback...\033[0m")
                os.system(f"nmap -sn {target}")
        except:
            print("\033[91m❌ Kernel Access Denied.\033[0m")
    else:
        print("\033[91m[!] No response on common ports. Device is in Deep Stealth.\033[0m")

    print("\033[92m✅ Socket Audit Complete.\033[0m")