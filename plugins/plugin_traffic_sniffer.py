import subprocess, os

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    print(f"{Y}[*] Initializing Traffic Sniffer (Ghost-Mode)...{RS}")
    
    # Check for TShark (Standard Termux Sniffer)
    check_tshark = subprocess.run("command -v tshark", shell=True, capture_output=True)
    
    if check_tshark.returncode != 0:
        print(f"{R}[!] Error: 'tshark' is not installed.{RS}")
        print(f"{G}[i] Run: pkg install tshark -y{RS}")
        return

    print(f"{G}[✓] Sniffer Engine: ONLINE{RS}")
    print(f"{Y}[!] Capturing 20 packets from local interface...{RS}\n")
    
    try:
        # Capture summary of traffic (IPs and Protocols)
        # -c 20: capture 20 packets
        # -T fields: output specific data points
        cmd = "tshark -c 20 -T fields -e ip.src -e ip.dst -e _ws.col.Protocol"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if process.stdout:
            print(f"{G}SOURCE IP       | DESTINATION IP  | PROTOCOL{RS}")
            print(f"----------------|-----------------|-----------")
            print(process.stdout)
        else:
            print(f"{R}[!] No traffic detected. Ensure you are on a busy network.{RS}")
            
    except Exception as e:
        tools.log_error("Sniffer-Core", str(e))
    
    tools.show_report()

if 'tools' in globals():
    run(tools)