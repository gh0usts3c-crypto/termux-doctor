import os
import subprocess

def run():
    target = input("\033[93m[?] Target IP for Native-Z Audit: \033[0m").strip()
    if not target: return

    # Common Stealth Ports
    ports = "80 443 22 135 445 8080"
    
    print(f"\033[93m[*] Forcing Native-Z Handshake on {target}...\033[0m")
    
    # -z: Zero-I/O (Handshake only), -w1: 1 second timeout, -v: Verbose
    # We use 'sh' to bypass Python's socket restrictions
    cmd = f"nc -zv -w1 {target} {ports} 2>&1"
    
    try:
        output = subprocess.check_output(cmd, shell=True).decode()
        print(output)
        
        if "succeeded" in output.lower() or "open" in output.lower():
            print(f"\033[92m[+] [SYSTEM-SUCCESS] Handshake Confirmed.\033[0m")
            print("\033[94m[*] Checking Kernel ARP Table for Identity...\033[0m")
            os.system(f"ip neigh show {target}")
        else:
            print("\033[91m[!] No open gates found on common ports.\033[0m")
            
    except Exception:
        print("\033[91m❌ Native Handshake Failed to execute.\033[0m")
        print("💡 Suggestion: Run 'setup tools' to ensure 'netcat' is installed.")

    print("\033[92m✅ Native Audit Complete.\033[0m")