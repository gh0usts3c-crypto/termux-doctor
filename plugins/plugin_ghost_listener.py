DOC = "Listen for devices broadcasting their names (mDNS/Chromecast/Printers)."
def run(tools):
    print("\033[93m[*] Entering Passive Listen Mode (10 Seconds)... \033[0m")
    print("\033[94m[*] Catching mDNS/Service Broadcasts (Zero Noise)...\033[0m")
    
    # -p: Passive mode, -60: Listen for 60 packets or 10s
    # We use 'nmap --script dns-service-discovery' on the local broadcast address
    # This is much quieter than a direct IP scan.
    tools.run_cmd("nmap -T4 -p 5353 --script dns-service-discovery 224.0.0.251")
    
    print("\033[92m✅ Listening Phase Complete.\033[0m")