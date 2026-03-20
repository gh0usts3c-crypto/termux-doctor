import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

# THE PROFESSIONAL PERSONA (The "Brain" Filter)
SYSTEM_PROMPT = (
    "Role: Senior Termux & Linux Security Expert. "
    "Style: Professional, concise, technical. No conversational filler or 'certainly'/'here is'. "
    "Output: Direct answers, minimal text, maximum code/commands. "
    "Constraints: Use Markdown for code blocks. Prioritize Termux-compatible tools (pkg over apt). "
    "Security: Flag potentially dangerous commands with a [!] warning."
)

def print_banner(ai_status):
    os.system('clear')
    status_text = f"{G}ON (PRO-MODE){RS}" if ai_status else f"{R}OFF (STEALTH){RS}"
    print(f"{G}{' TERMUX-DOCTOR v3.0 '.center(40, '=')}{RS}")
    print(f"{Y}{f'[ AI ENGINE: {status_text} ]'.center(40)}{RS}\n")

def main():
    ai_enabled = True
    print_banner(ai_enabled)
    
    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        p_color, p_label = (G, "Dr. Prompt") if ai_enabled else (R, "[STEALTH]")
        user_input = input(f"{p_color}{p_label} > {RS}").strip()
        
        if not user_input: continue
        cmd = user_input.lower()

        if cmd in ['exit', 'quit']: sys.exit(0)
        if cmd == 'ai off': ai_enabled = False; print_banner(ai_enabled); continue
        if cmd == 'ai on': ai_enabled = True; print_banner(ai_enabled); continue
        if cmd == 'clear': print_banner(ai_enabled); continue

        if not ai_enabled:
            print(f"{Y}[STEALTH ECHO]:{RS} {user_input}\n")
            continue

        if not api_key:
            print(f"{R}❌ No Key. Use 'update key'.{RS}")
            continue

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            print(f"{Y}[*] Establishing Handshake...{RS}", end="\r")
            
            # Sending the SYSTEM_PROMPT to force professional behavior
            response = client.chat.completions.create(
                model="openrouter/free", 
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                timeout=20.0
            )
            print(" " * 30, end="\r")
            print(f"\n{Y}👨‍⚕️ [Doctor]:{RS}\n{response.choices[0].message.content}\n")
        except Exception as e:
            print(f"{R}❌ Error: {e}{RS}")

if __name__ == '__main__':
    main()