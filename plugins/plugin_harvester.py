# DOCTOR-NATIVE MODULE v4.2
DOC = "Native ARP Harvester: Maps hardware IDs (MAC) to IPs on the local WiFi."

def run(tools):
    # Pulling colors from the Doctor's core logic
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    
    print(f"{Y}[*] Termux-Doctor: Initiating Native Harvest...{RS}")
    
    # Using the Doctor's central subnet engine
    subnet = tools.get_subnet()
    print(f"{G}[+] Target Subnet: {subnet}{RS}")
    
    # Using the Doctor's stealth execution engine
    # We refresh the ARP table with a quiet 'ping-only' sweep
    print(f"{Y}[*] Refreshing system neighbor table...{RS}")
    tools.run_cmd(f"nmap -sn {subnet}", silent=True)
    
    print(f"\n{G}--- ACTIVE NETWORK INVENTORY ---{RS}")
    
    # Direct Kernel Interrogation
    # This pulls from the device's internal memory (Passive)
    tools.run_cmd("ip neigh show | grep -v 'FAILED' | grep -v 'INCOMPLETE'")
    
    print(f"\n{Y}💡 Analysis Complete. These devices are physically on your WiFi.{RS}")