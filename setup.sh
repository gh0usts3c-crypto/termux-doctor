#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting Termux-Doctor Bulletproof Install..."

# 1. Set Environment Variables for Rust/Pydantic
export ANDROID_API_LEVEL=26

# 2. Install Pre-compiled System Binaries (The 'Metadata' Fix)
pkg update -y && pkg upgrade -y
pkg install python python-cryptography python-pydantic python-pydantic-core python-typing-extensions clang rust binutils git termux-api -y

# 3. Upgrade build tools
pip install --upgrade pip setuptools wheel

# 4. Install AI Core
echo "📦 Finalizing AI Core... this should now bypass metadata errors."
pip install google-generativeai

# 5. Repository Sync
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
rm -rf ~/.termux_doctor
git clone $REPO_URL ~/.termux_doctor

# 6. Alias Setup
if ! grep -q "alias doctor=" ~/.bashrc; then
    echo "alias doctor='python ~/.termux_doctor/core/main.py'" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ Deployment Successful! Type 'doctor' to launch."
