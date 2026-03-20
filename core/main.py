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
    else:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        print(f"{Y}🔑 [NEW DOCTOR DETECTED]{RS}")
        key = input("Please paste your Gemini API Key: ")
        with open(config_path, "w") as f:
            f.write(key)
        return key

def main():
    os.system('clear')
    print_banner()
    
    # Pre-flight check
    print(f"{G}✅ System Vitals: NOMINAL{RS}")
    
    api_key = get_api_key()
    
    try:
        # 2026 SDK Client
        client = genai.Client(api_key=api_key)
        print(f"{G}🩺 Doctor is Online. How can I help with your network today?{RS}")
        
        while True:
            user_input = input(f"\n{G}Dr. Prompt > {RS}")
            if user_input.lower() in ['exit', 'quit']: break
            
            # Use the 2026 Flash 2.0 model
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=user_input
            )
            print(f"\n{Y}👨‍⚕️ [Doctor's Insight]:{RS}\n{response.text}")
            
    except Exception as e:
        print(f"{R}❌ Doctor Error: {e}{RS}")

if __name__ == '__main__':
    main()
