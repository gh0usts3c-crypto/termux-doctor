# DOCTOR-NATIVE MODULE v4.3.2
DOC = "Advanced ID Resolver: Decodes Privacy-Masked and Generic IoT hardware."

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    
    # MASTER DATABASE EXTENSION
    OUI_MAP = {
        "FC:65:DE": "Apple", "F0:99:BF": "Apple", "00:23:12": "Apple", 
        "00:05:CD": "Samsung", "A4:77:33": "Google", "44:65:0D": "Amazon",
        "D8:07:B6": "TP-Link", "B8:27:EB": "Raspberry Pi", "DC:A6:32": "Raspberry Pi",
        "AC:CF:85": "Espressif (IoT)", "D0:73:D5": "Espressif", "2C:F4:32": "Espressif",
        "04:CF:8C": "Shenzhen/Tuya (Generic Smart Home)", "BC:DD:C2": "Xiaomi",
        "18:EC:E7": "Tesla", "50:14:79": "Ring", "14:4F:8A": "Sonos"
    }

    print(f"{Y}[*] Termux-Doctor: Finalizing Identity Matrix...{RS}")
    
    import subprocess
    try:
        raw_neigh = subprocess.check_output("ip neigh show", shell=True).decode()
        
        print(f"\n{G}IP ADDRESS      |  RECONNAISSANCE IDENTITY{RS}")
        print(f"{G}----------------|-------------------------{RS}")
        
        for line in raw_neigh.split('\n'):
            if 'lladdr' in line and 'REACHABLE' in line:
                parts = line.split()
                ip = parts[0]
                mac = parts[parts.index('lladdr') + 1].upper()
                prefix = mac[:8]
                
                # BITMASK ANALYSIS
                first_byte = int(mac[:2], 16)
                if (first_byte & 0x02):
                    vendor = f"{Y}[PRIVACY-MASKED]{RS} (High-Security Phone/PC)"
                else:
                    vendor = OUI_MAP.get(prefix, f"{R}Generic/IoT ({prefix}){RS}")
                
                print(f"{ip:<15} |  {vendor}")
                
    except Exception as e:
        print(f"{R}❌ Logic Error: {e}{RS}")