#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting Phoenix Reinstall..."

# 1. Clean up old artifacts
rm -rf ~/.termux_doctor
rm -rf ~/.config/termux_doctor

# 2. System-Level Dependencies (The 2026 'Magic' List)
pkg update -y && pkg upgrade -y
pkg install unstable-repo x11-repo -y
pkg update
pkg install python python-cryptography python-pydantic python-grpcio \
            python-typing-extensions clang rust binutils git termux-api -y

# 3. Environment Variable Injection
export ANDROID_API_LEVEL=26
export PYTHONPATH=$PYTHONPATH:/data/data/com.termux/files/usr/bin/python3.11/site-packages

# 4. Pip Force-Link (Fixes the 'No module named google' error)
pip install --upgrade pip setuptools wheel
echo "📦 Injecting AI Core and Google Namespace..."
pip install google-api-core
pip install google-generativeai --no-build-isolation

# 5. Repository Sync
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
git clone $REPO_URL ~/.termux_doctor

# 6. Global Alias Update
if ! grep -q "alias doctor=" ~/.bashrc; then
    echo "alias doctor='PYTHONPATH=/data/data/com.termux/files/usr/lib/python3.11/site-packages python ~/.termux_doctor/core/main.py'" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ PHOENIX DEPLOYMENT COMPLETE! Type 'doctor'."
