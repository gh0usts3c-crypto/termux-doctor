import os
def run():
    print("\033[93m[*] Executing Local Net Audit...\033[0m")
    os.system("ip addr | grep 'inet '")
    print("\033[92m✅ Local interface check complete.\033[0m")