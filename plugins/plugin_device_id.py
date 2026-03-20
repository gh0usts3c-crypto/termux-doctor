# DOCTOR-NATIVE MODULE v4.5 (Ghost-Protocol)
DOC = "Ghost ID: The most silent, verified identification method available."

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    import subprocess, socket

    print(f"{Y}[*] Termux-Doctor: Ghost Discovery Engaged...{RS}")
    
    try:
        # STEP 1: SILENT PULSE
        # --max-rate 10: Slows the pulse to 10 packets/sec (Looks like normal traffic)
        subnet = tools.get_subnet()
        tools.run_cmd(f"nmap -sn --max-rate 10 {subnet}", silent=True)
        
        # STEP 2: NATIVE KERNEL READ
        raw_neigh = subprocess.check_output("ip neigh show", shell=True).decode()
        
        print(f"\n{G}IP ADDRESS      | HW-VENDOR         | GHOST-PROBE CONFIRM{RS}")
        print(f"{G}----------------|-------------------|----------------------{RS}")
        
        for line in raw_neigh.split('\n'):
            if 'lladdr' in line and 'REACHABLE' in line:
                parts = line.split()
                ip = parts[0]
                mac = parts[parts.index('lladdr') + 1].upper()
                
                # OPTIMAL IDENTIFICATION (Bitmask check first)
                first_byte = int(mac[:2], 16)
                if (first_byte & 0x02):
                    vendor = "Privacy-Masked"
                    # CONFIRMATION VIA DISCOVERY PORTS (mDNS & Apple Sync)
                    # These are 'Discovery' ports, not 'Security' ports.
                    hint = f"{R}Shadow Device{RS}"
                    
                    # Check for Apple Service (62078)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)
                        if s.connect_ex((ip, 62078)) == 0:
                            hint = f"{G}Confirmed Apple{RS}"
                        elif s.connect_ex((ip, 5353)) == 0:
                            hint = f"{G}IoT/Smart Media{RS}"
                else:
                    # Known hardware vendors
                    prefix = mac[:8]
                    OUI = {"FC:65:DE":"Apple", "00:05:CD":"Samsung", "A4:77:33":"Google"}
                    vendor = OUI.get(prefix, f"Unlisted ({prefix})")
                    hint = f"{Y}Verified Hardware{RS}"

                print(f"{ip:<15} | {vendor:<17} | {hint}")
                
    except Exception as e:
        print(f"{R}❌ Audit Error: {e}{RS}")