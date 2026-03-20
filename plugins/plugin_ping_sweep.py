def run(tools):
    target = tools.get_subnet()
    print(f"\033[93m[*] Sweeping {target} (User-Mode)...\033[0m")
    tools.run_cmd(f"nmap -sn -PS80,443,22,445,8080 --max-retries 1 {target}")