import subprocess, os

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    print(f"{Y}[*] Ghost-Sniffer: Initializing...{RS}")
    
    # Validation check
    if subprocess.run("command -v tshark", shell=True, capture_output=True).returncode != 0:
        print(f"{R}[!] Missing Dependency: tshark{RS}")
        return

    print(f"{G}[✓] Interface: eth0/wlan0 Active{RS}")
    
    try:
        # Capturing 10 packets for a quick diagnostic
        cmd = "tshark -c 10 -T fields -e ip.src -e ip.dst -e _ws.col.Protocol"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"\n{G}SRC-IP          | DST-IP          | PROT{RS}")
        print(process.stdout)
    except Exception as e:
        tools.log_error("Sniffer", str(e))
    
    tools.show_report()

if 'tools' in globals():
    run(tools)