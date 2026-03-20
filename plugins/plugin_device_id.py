# DOCTOR-NATIVE MODULE v4.7
DOC = "Verified ID + Diagnostic: The most silent, verified identification method."

def run(tools):
    G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
    import subprocess, socket

    print(f"{Y}[*] Ghost Discovery Engaged...{RS}")
    
    try:
        subnet = tools.get_subnet()
        p = subprocess.run(f"nmap -sn --max-rate 10 {subnet}", shell=True, capture_output=True, text=True)
        if p.returncode != 0: tools.log_error("Pulse", p.stderr.strip())

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
                        s.settimeout(0.3)
                        if s.connect_ex((ip, 62078)) == 0: hint = f"{G}Confirmed Apple{RS}"
                except Exception as e: tools.log_error(f"Socket-{ip}", str(e))
                
                print(f"{ip:<15} | {mac[:8]:<17} | {hint}")
                
    except Exception as e:
        tools.log_error("Identity-Logic", str(e))

    tools.show_report()