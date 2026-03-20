import os
import sys
import shutil
from openai import OpenAI

G, Y, R, RS = "\033[92m", "\033[93m", "\033[91m", "\033[0m"
CONFIG_PATH = os.path.expanduser("~/.config/termux_doctor/openrouter.key")

# UPDATED 2026 FREE ENDPOINTS
MODEL_LIST = [
    "meta-llama/llama-3-8b-instruct:free",
    "google/gemini-pro-1.5",
    "mistralai/mistral-7b-instruct:free",
    "openrouter/auto" # OpenRouter's internal 'best free model' router
]

def main():
    os.system('clear')
    print(f"{G}TERMUX-DOCTOR v2.6{RS}")
    print(f"{Y}[ STANDBY: WAITING FOR HEARTBEAT ]{RS}\n")

    while True:
        api_key = None
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f: api_key = f.read().strip()

        user_input = input(f"{G}Dr. Prompt > {RS}").strip()
        if not user_input or user_input.lower() in ['exit', 'quit']: sys.exit(0)
        
        if user_input.lower() == 'update key':
            val = input(f"🔑 Key: ").strip()
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f: f.write(val)
            print("✅ Key Saved.")
            continue

        if not api_key:
            print(f"{R}❌ No Key found.{RS}")
            continue

        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        
        success = False
        for model_id in MODEL_LIST:
            try:
                # v2.6 adds a timeout and more robust headers
                response = client.chat.completions.create(
                    model=model_id, 
                    messages=[{"role": "user", "content": user_input}],
                    timeout=15.0
                )
                print(f"\n{Y}👨‍⚕️ [Doctor ({model_id})]:{RS}\n{response.choices[0].message.content}\n")
                success = True
                break
            except Exception as e:
                # Silently try next model unless it's the last one
                if model_id == MODEL_LIST[-1]:
                    print(f"{R}❌ Final Attempt Failed: {e}{RS}")
        
        if not success:
            print(f"{Y}💡 DIAGNOSIS: Visit https://openrouter.ai/activity to see why the request was blocked.{RS}")

if __name__ == '__main__':
    main()