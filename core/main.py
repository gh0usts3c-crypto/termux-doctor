import os
import sys
import subprocess
import google.generativeai as genai
from core.config_mgr import load_api_key

# DNA Banner Colors
G = "\033[92m"  # Green
Y = "\033[93m"  # Yellow
R = "\033[0m"   # Reset

def print_banner():
    banner = f"""
{G}      .      .{Y}        _____________________________________________{R}
{G}     / \    / \{Y}      |                                             |{R}
{G}    /   \__/   \{Y}     |{G}               TERMUX-DOCTOR{Y}                 |{R}
{G}    \   /  \   /{Y}     |{G}        > Network DNA Analysis v1.0 <{Y}        |{R}
{G}     \_/    \_/{Y}      |_____________________________________________|{R}
{G}      |      |{R}       
{G}      |      |{R}       {Y}[ STATUS: SCANNING VITAL SIGNS... ]{R}
    """
    print(banner)

def update_system():
    print("🔄 Checking for updates from GitHub...")
    try:
        repo_path = os.path.expanduser("~/.termux_doctor")
        if os.path.exists(repo_path):
            os.chdir(repo_path)
            output = subprocess.check_output(["git", "pull", "origin", "main"]).decode('utf-8')
            if "Already up to date" in output:
                print("✅ Termux-Doctor is already at the latest version.")
            else:
                print("🚀 Update successful! Restarting...")
                os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"❌ Update failed: {e}")

def main():
    if "--update" in sys.argv:
        update_system()
        return

    print_banner()
    api_key = load_api_key()
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        while True:
            user_input = input(f"\n{G}Dr. Prompt > {R}")
            if user_input.lower() in ['exit', 'quit']: break
            if user_input.lower() == '--update':
                update_system()
                continue
            
            response = model.generate_content(f"Analyze this net-testing request: {user_input}")
            print(f"\n{Y}👨‍⚕️ [Doctor's Insight]:{R}\n{response.text}")
            
    except Exception as e:
        print(f"❌ Gemini Error: {e}")

if __name__ == '__main__':
    main()
