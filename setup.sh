#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting Advanced System Repair..."

# 1. Enable TUR (Termux User Repository) - This is where Pydantic lives now
pkg update -y
pkg install tur-repo -y
pkg update

# 2. Install the modern binaries from TUR
# This bypasses the Rust/Metadata issue entirely
pkg install python python-cryptography python-pydantic-core clang rust git -y

# 3. Install the NEW 2026 Google GenAI SDK
# Note: 'google-generativeai' is being replaced by 'google-genai'
pip install --upgrade pip
pip install google-genai

# 4. Refresh Repository
rm -rf ~/.termux_doctor
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor

echo "alias doctor='python ~/.termux_doctor/core/main.py'" > ~/.termux_doctor_alias
if ! grep -q "termux_doctor_alias" ~/.bashrc; then
    echo "source ~/.termux_doctor_alias" >> ~/.bashrc
fi
source ~/.bashrc

python ~/.termux_doctor/core/main.py
