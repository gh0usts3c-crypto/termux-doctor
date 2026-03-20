import subprocess, socket

def run(tools):
    G, Y, RS = "\033[92m", "\033[93m", "\033[0m"
    print(f"{Y}[*] Discovering Network Ghosts...{RS}")
    try:
        subnet = tools.get_subnet()
        subprocess.run(f"nmap -sn --max-rate 10 {subnet}", shell=True, capture_output=True)
        raw_neigh = subprocess.check_output("ip neigh show", shell=True).decode()
        
        print(f"\n{G}IP ADDRESS      | HW-VENDOR         | PROBE{RS}")
        print(f"{G}----------------|-------------------|------------{RS}")
        
        for line in raw_neigh.split('\n'):
            if 'lladdr' in line and 'REACHABLE' in line:
                parts = line.split()
                ip, mac = parts[0], parts[parts.index('lladdr') + 1].upper()
                hint = "Idle"
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.2)
                        if s.connect_ex((ip, 62078)) == 0: hint = f"{G}Confirmed Apple{RS}"
                except: pass
                print(f"{ip:<15} | {mac[:8]:<17} | {hint}")
    except Exception as e: tools.log_error("Identity-Logic", str(e))
    tools.show_report()

if 'tools' in globals():
    run(tools)