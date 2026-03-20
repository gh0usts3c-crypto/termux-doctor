# DOCTOR-NATIVE MODULE v4.3
DOC = "Translates MAC addresses into Manufacturer Names (Apple, Samsung, etc)."

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    
    # Local OUI Dictionary (Top Manufacturers for Stealth/Speed)
    OUI_MAP = {
        "3C:D9:2B": "HP (Hewlett-Packard)",
        "00:0C:29": "VMware",
        "00:14:22": "Dell",
        "00:05:CD": "Samsung",
        "B8:27:EB": "Raspberry Pi",
        "DC:A6:32": "Raspberry Pi",
        "00:17:88": "Philips Hue",
        "AC:CF:85": "Espressif (IoT)",
        "D0:73:D5": "Espressif (IoT)",
        "00:25:90": "Supermicro",
        "00:11:32": "Synology",
        "00:1D:C9": "Garmin",
        "BC:5F:F4": "ASRock",
        "E4:E7:49": "Sony",
        "FC:65:DE": "Apple",
        "F0:99:BF": "Apple",
        "00:23:12": "Apple",
        "44:65:0D": "Amazon (Echo/Kindle)",
        "A4:77:33": "Google",
        "D8:07:B6": "TP-Link",
        "00:03:7F": "Atheros (Qualcomm)"
    }

    print(f"{Y}[*] Termux-Doctor: Resolving Network Identities...{RS}")
    
    # 1. Refresh Table
    subnet = tools.get_subnet()
    tools.run_cmd(f"nmap -sn {subnet}", silent=True)
    
    # 2. Get Raw Neighbor Table
    import subprocess
    try:
        raw_neigh = subprocess.check_output("ip neigh show", shell=True).decode()
        
        print(f"\n{G}IP ADDRESS      |  MANUFACTURER / IDENTITY{RS}")
        print(f"{G}----------------|-------------------------{RS}")
        
        for line in raw_neigh.split('\n'):
            if 'lladdr' in line and 'REACHABLE' in line:
                parts = line.split()
                ip = parts[0]
                mac = parts[parts.index('lladdr') + 1].upper()
                prefix = mac[:8] # First 3 Octets (OUI)
                
                vendor = OUI_MAP.get(prefix, "Unknown / Randomized MAC")
                
                # Check for Randomized MACs (Common in Android/iOS)
                # Bit 2 of first octet being 1 indicates 'Locally Administered'
                first_octet = int(mac[:2], 16)
                if (first_octet & 2):
                    vendor = f"{Y}Private (Privacy-Randomized){RS}"
                
                print(f"{ip:<15} |  {vendor}")
                
    except Exception as e:
        print(f"{R}❌ Identity Resolution Failed: {e}{RS}")

    print(f"\n{Y}💡 Tip: Randomized MACs are standard on modern mobile devices for privacy.{RS}")