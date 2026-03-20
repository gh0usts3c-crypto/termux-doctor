DOC = "Fingerprints device OS and services (HTTP, SSH, SMB, etc)."
def run(tools):
    target = input("\033[93m[?] Enter Target IP to Audit: \033[0m").strip()
    if not target: return

    print(f"\033[93m[*] Auditing {target}... (Low-Intensity Service Scan)\033[0m")
    
    # -sV: Version Detection, -O: OS Detection (Best Effort), -T3: Balanced
    # --top-ports 100: Only scans most likely services to keep it fast/quiet
    tools.run_cmd(f"nmap -sV -O --top-ports 100 --max-retries 1 {target}")
    
    print("\033[92m✅ Audit Complete.\033[0m")