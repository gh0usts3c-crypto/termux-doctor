import os
import google.generativeai as genai
from core.config_mgr import load_api_key

def main():
    print("🩺 Termux-Doctor: Diagnostic System Online.")
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    while True:
        user_input = input("\nDr. Prompt > ")
        if user_input.lower() in ['exit', 'quit']: break
        
        # Send to Gemini with Security Analyst context
        response = model.generate_content(f"Analyze this net-testing request: {user_input}")
        print(f"\n👨‍⚕️ [Doctor's Insight]:\n{response.text}")

if __name__ == '__main__':
    main()
