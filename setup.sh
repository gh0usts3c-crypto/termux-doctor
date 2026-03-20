#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Performing Absolute Path Reconstruction..."

# 1. Purge and Refresh
rm -rf ~/.termux_doctor
pkg update -y
pkg install python git clang rust binutils -y

# 2. Get the Dynamic Python Path
PY_VER=3.14
PY_PATH="/data/data/com.termux/files/usr/lib/python$PY_VER/site-packages"

# 3. Force-Install the 'Google' Namespace into that path
pip install --upgrade pip
pip install google-api-core google-generativeai

# 4. Clone and Create the Global Alias with Dynamic Pathing
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
git clone $REPO_URL ~/.termux_doctor

# We write the alias to handle the PYTHONPATH automatically
echo "alias doctor='PYTHONPATH=$PY_PATH python ~/.termux_doctor/core/main.py'" > ~/.termux_doctor_alias
if ! grep -q "termux_doctor_alias" ~/.bashrc; then
    echo "source ~/.termux_doctor_alias" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ Absolute Fix Applied. Type 'doctor' to test."
