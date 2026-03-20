# DOCTOR-NATIVE MODULE v4.3.3
DOC = "Active ID Resolver: Pulses the network to wake up silent devices."

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    
    OUI_MAP = {
        "FC:65:DE": "Apple", "F0:99:BF": "Apple", "00:23:12": "Apple", 
        "00:05:CD": "Samsung", "A4:77:33": "Google", "44:65:0D": "Amazon",
        "D8:07:B6": "TP-Link", "B8:27:EB": "Raspberry Pi", "DC:A6:32": "Raspberry Pi",
        "AC:CF:85": "Espressif (IoT)", "04:CF:8C": "Shenzhen/Tuya (IoT)",
        "18:EC:E7": "Tesla", "50:14:79": "Ring", "14:4F:8A": "Sonos"
    }

    print(f"{Y}[*] Termux-Doctor: Pulsing network to wake neighbors...{RS}")
    
    import subprocess
    try:
        # 1. THE PULSE: Force a fresh ARP population
        subnet = tools.get_subnet()
        # -sn (No port scan) -n (No DNS) --send-ip (Avoids raw sockets/root issues)
        tools.run_cmd(f"nmap -sn -n {subnet}", silent=True)
        
        # 2. THE HARVEST: Read the now-populated table
        raw_neigh = subprocess.check_output("ip neigh show", shell=True).decode()
        
        print(f"\n{G}IP ADDRESS      |  RECONNAISSANCE IDENTITY{RS}")
        print(f"{G}----------------|-------------------------{RS}")
        
        found = False
        for line in raw_neigh.split('\n'):
            # Look for devices that are REACHABLE, STALE, or DELAY (all active)
            if 'lladdr' in line and any(state in line for state in ['REACHABLE', 'STALE', 'DELAY']):
                parts = line.split()
                ip = parts[0]
                mac = parts[parts.index('lladdr') + 1].upper()
                prefix = mac[:8]
                
                # BITMASK ANALYSIS
                first_byte = int(mac[:2], 16)
                if (first_byte & 0x02):
                    vendor = f"{Y}[PRIVACY-MASKED]{RS} (Android/iOS)"
                else:
                    vendor = OUI_MAP.get(prefix, f"{R}Unlisted OUI ({prefix}){RS}")
                
                print(f"{ip:<15} |  {vendor}")
                found = True
        
        if not found:
            print(f"{R}[!] No neighbors responded. Check WiFi connection.{RS}")
                
    except Exception as e:
        print(f"{R}❌ Logic Error: {e}{RS}")