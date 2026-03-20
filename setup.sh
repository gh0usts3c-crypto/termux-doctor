#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting Termux-Doctor Anti-Freeze Install..."

# 1. Install EVERYTHING that usually requires a slow Rust/C++ build
pkg update -y && pkg upgrade -y
pkg install python python-cryptography python-pydantic python-typing-extensions clang rust binutils git termux-api -y

# 2. Upgrade build tools
pip install --upgrade pip setuptools wheel

# 3. Install AI Core (Should be instant now as dependencies are met)
echo "📦 Finalizing AI Core..."
pip install google-generativeai

# 4. Repository Sync
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
rm -rf ~/.termux_doctor
git clone $REPO_URL ~/.termux_doctor

# 5. Alias Setup
if ! grep -q "alias doctor=" ~/.bashrc; then
    echo "alias doctor='python ~/.termux_doctor/core/main.py'" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ Success! Dr. Prompt is ready. Type 'doctor'."
