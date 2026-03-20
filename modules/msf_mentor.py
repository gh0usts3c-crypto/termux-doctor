import subprocess

def run_diagnostic():
    print("🩺 Dr. Insight: Analyzing Metasploit Environment...")
    # Checking if msfconsole is installed
    try:
        subprocess.run(["msfconsole", "-v"], check=True, capture_output=True)
        return "Metasploit is installed and ready for a lesson."
    except FileNotFoundError:
        return "Metasploit is NOT installed. Suggestion: 'pkg install metasploit'"

metadata = {
    "name": "Metasploit Mentor",
    "command": "msf-check",
    "description": "Educational guide for Metasploit Framework"
}
