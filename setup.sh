#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting High-Speed Diagnostic Install..."

# 1. Update system
pkg update -y && pkg upgrade -y
pkg install python clang rust git binutils -y

# 2. INSTALL PRE-COMPILED PYDANTIC-CORE (The Speed Hack)
echo "⚡ Downloading pre-built Android binaries..."
pip install pydantic-core --extra-index-url https://eutalix.github.io/android-pydantic-core/

# 3. Install remaining AI components
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

echo "✅ Speed Hack Applied! Type 'doctor'."
