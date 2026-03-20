import os
import sys
import subprocess

# Colors
G = "\033[92m"  # Green
Y = "\033[93m"  # Yellow
R = "\033[91m"  # Red
RS = "\033[0m"  # Reset

def check_vitals():
    print(f"{Y}[*] Checking System Vital Signs...{RS}")
    vitals = {
        "Python Version": "python --version",
        "Cryptography": "python -c 'import cryptography' 2>/dev/null",
        "Pydantic": "python -c 'import pydantic' 2>/dev/null",
        "Google AI Core": "python -c 'import google.generativeai' 2>/dev/null"
    }
    
    all_clear = True
    for name, cmd in vitals.items():
        exit_code = os.system(cmd)
        if exit_code == 0:
            print(f"  {G}✅ {name}: OK{RS}")
        else:
            print(f"  {R}❌ {name}: NOT FOUND or BROKEN{RS}")
            all_clear = False
    
    if not all_clear:
        print(f"\n{R}🚨 DIAGNOSTIC FAILURE:{RS}")
        print(f"{Y}Your Python environment is missing core organs.{RS}")
        print(f"Try running: {G}pkg install python-cryptography python-pydantic{RS}")
        sys.exit(1)

def print_banner():
    banner = f"""
{G}      .      .{Y}        _____________________________________________{RS}
{G}     / \    / \{Y}      |                                             |{RS}
{G}    /   \__/   \{Y}     |{G}               TERMUX-DOCTOR{Y}                 |{RS}
{G}    \   /  \   /{Y}     |{G}        > Network DNA Analysis v1.0 <{Y}        |{RS}
{G}     \_/    \_/{Y}      |_____________________________________________|{RS}
{G}      |      |{RS}       
{G}      |      |{RS}       {Y}[ STATUS: SCANNING VITAL SIGNS... ]{RS}
    """
    print(banner)

def main():
    print_banner()
    check_vitals()
    
    # If vitals pass, proceed to import and run
    try:
        import google.generativeai as genai
        from core.config_mgr import load_api_key
        
        api_key = load_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print(f"{G}🩺 Dr. Prompt is Online.{RS}")
        while True:
            user_input = input(f"\n{G}Dr. Prompt > {RS}")
            if user_input.lower() in ['exit', 'quit']: break
            response = model.generate_content(user_input)
            print(f"\n{Y}👨‍⚕️ [Doctor's Insight]:{RS}\n{response.text}")
            
    except Exception as e:
        print(f"{R}❌ Runtime Error: {e}{RS}")

if __name__ == '__main__':
    main()
