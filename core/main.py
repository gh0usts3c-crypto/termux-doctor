import os
import sys
from google import genai

def check_vitals():
    print("\033[93m[*] Checking 2026 Standard Vitals...\033[0m")
    try:
        import cryptography
        print("\033[92m  ✅ Cryptography: OK\033[0m")
        from google import genai
        print("\033[92m  ✅ Google GenAI SDK: OK\033[0m")
    except Exception as e:
        print(f"\033[91m  ❌ Vital Failure: {e}\033[0m")
        sys.exit(1)

def main():
    check_vitals()
    # Updated 2026 Client Init
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "YOUR_KEY_HERE"))
    print("\033[92m🩺 Doctor is Online.\033[0m")
    
    while True:
        user_input = input("\n\033[92mDr. Prompt > \033[0m")
        if user_input.lower() in ['exit', 'quit']: break
        response = client.models.generate_content(model="gemini-2.0-flash", contents=user_input)
        print(f"\n\033[93m👨‍⚕️ [Doctor's Insight]:\033[0m\n{response.text}")

if __name__ == '__main__':
    main()
