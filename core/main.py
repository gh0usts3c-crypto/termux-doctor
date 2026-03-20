import os
import sys
from google import genai

# DNA Banner Colors
G = "\033[92m"  # Green
Y = "\033[93m"  # Yellow
R = "\033[91m"  # Red
RS = "\033[0m"  # Reset

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

def get_api_key():
    config_path = os.path.expanduser("~/.config/termux_doctor/gemini.key")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return f.read().strip()
    return None

def main():
    os.system('clear')
    print_banner()
    
    api_key = get_api_key()
    if not api_key:
        print(f"{R}❌ No API Key found. Run the setup again.{RS}")
        sys.exit(1)
    
    try:
        # 2026 GenAI SDK Client
        client = genai.Client(api_key=api_key)
        
        # WE ARE NOW USING THE 2026 STABLE FLASH MODEL
        # Options: "gemini-2.5-flash" or "gemini-3-flash-preview"
        ACTIVE_MODEL = "gemini-2.5-flash"
        
        print(f"{G}🩺 Doctor is Online using {ACTIVE_MODEL}.{RS}")
        
        while True:
            user_input = input(f"\n{G}Dr. Prompt > {RS}")
            if user_input.lower() in ['exit', 'quit']: break
            
            # API Call with 2026 Parameters
            response = client.models.generate_content(
                model=ACTIVE_MODEL, 
                contents=user_input
            )
            print(f"\n{Y}👨‍⚕️ [Doctor's Insight]:{RS}\n{response.text}")
            
    except Exception as e:
        # Detailed error reporting for debugging
        print(f"{R}❌ Doctor Error: {e}{RS}")
        if "API key not valid" in str(e):
            print(f"{Y}💡 Tip: Check if billing is enabled or try a new key from AI Studio.{RS}")

if __name__ == '__main__':
    main()
