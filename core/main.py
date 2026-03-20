import os
import sys
import subprocess
import google.generativeai as genai
from core.config_mgr import load_api_key

def update_system():
    print("🔄 Checking for updates from GitHub...")
    try:
        # Navigate to the install directory in Termux and pull
        repo_path = os.path.expanduser("~/.termux_doctor")
        if os.path.exists(repo_path):
            os.chdir(repo_path)
            output = subprocess.check_output(["git", "pull", "origin", "main"]).decode('utf-8')
            if "Already up to date" in output:
                print("✅ Termux-Doctor is already at the latest version.")
            else:
                print("🚀 Update successful! Restarting...")
                os.execv(sys.executable, ['python'] + sys.argv)
        else:
            print("❌ Error: Install directory not found. Run setup.sh again.")
    except Exception as e:
        print(f"❌ Update failed: {e}")

def main():
    if "--update" in sys.argv:
        update_system()
        return

    print("\n🩺 Termux-Doctor: Diagnostic System Online.")
    api_key = load_api_key()
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Tip: Type '--update' to sync new modules from GitHub.")
        
        while True:
            user_input = input("\nDr. Prompt > ")
            if user_input.lower() in ['exit', 'quit']: break
            if user_input.lower() == '--update':
                update_system()
                continue
            
            # Send to Gemini with Security Analyst context
            response = model.generate_content(f"Analyze this net-testing request: {user_input}")
            print(f"\n👨‍⚕️ [Doctor's Insight]:\n{response.text}")
            
    except Exception as e:
        print(f"❌ Gemini Error: {e}")

if __name__ == '__main__':
    main()
