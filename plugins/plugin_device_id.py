# DOCTOR-NATIVE MODULE v4.4 (Verified)
DOC = "Verified ID: Uses MAC + Service Fingerprinting for high-accuracy identification."

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    import subprocess
    
    # 1. SHARED HARDWARE MAP
    OUI_MAP = {
        "FC:65:DE": "Apple", "00:05:CD": "Samsung", "A4:77:33": "Google", 
        "44:65:0D": "Amazon", "D8:07:B6": "TP-Link", "B8:27:EB": "Raspberry Pi"
    }

    print(f"{Y}[*] Termux-Doctor: Initiating Verified Discovery...{RS}")
    
    try:
        # STEP 1: PULSE & PROBE (Unified Action)
        # -sn: Discovery, -PS80,443: TCP Ping to verify service presence
        subnet = tools.get_subnet()
        tools.run_cmd(f"nmap -sn -PS80,443,22,62078 {subnet}", silent=True)
        
        # STEP 2: HARVEST KERNEL DATA
        raw_neigh = subprocess.check_output("ip neigh show", shell=True).decode()
        
        print(f"\n{G}IP ADDRESS      | HW-VENDOR         | SERVICE HINT{RS}")
        print(f"{G}----------------|-------------------|----------------------{RS}")
        
        for line in raw_neigh.split('\n'):
            if 'lladdr' in line and 'REACHABLE' in line:
                parts = line.split()
                ip = parts[0]
                mac = parts[parts.index('lladdr') + 1].upper()
                prefix = mac[:8]
                
                # Identify via MAC
                first_byte = int(mac[:2], 16)
                if (first_byte & 0x02):
                    vendor = "Privacy-Masked"
                else:
                    vendor = OUI_MAP.get(prefix, "Unknown")

                # SERVICE VERIFICATION (The Accuracy Layer)
                # We check if Port 62078 is open (Apple) or 80 (Web/Router)
                hint = "Idle/Hidden"
                if "Privacy-Masked" in vendor:
                    # Quick check to see if it's an iPhone/iPad
                    res = subprocess.getoutput(f"nc -zv -w 1 {ip} 62078 2>&1")
                    if "succeeded" in res: hint = f"{G}Confirmed Apple Device{RS}"
                    else:
                        res = subprocess.getoutput(f"nc -zv -w 1 {ip} 80 2>&1")
                        if "succeeded" in res: hint = f"{Y}Web-Enabled (PC/IoT){RS}"

                print(f"{ip:<15} | {vendor:<17} | {hint}")
                
    except Exception as e:
        print(f"{R}❌ Logic Error: {e}{RS}")