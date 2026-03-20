#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting Termux-Doctor Optimized Install..."

# 1. Repos and System updates
pkg update -y && pkg upgrade -y
pkg install unstable-repo x11-repo -y
pkg update

# 2. Install ALL heavy C++/Rust binaries via 'pkg' to avoid 'pip' builds
pkg install python python-cryptography python-pydantic python-grpcio clang rust binutils git termux-api -y

# 3. Finalize AI Core using system-linked libraries
pip install --upgrade pip setuptools wheel
echo "📦 Finalizing AI Core... (Optimized for pre-compiled binaries)"
pip install google-generativeai --no-build-isolation

# 4. Repository Sync
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
rm -rf ~/.termux_doctor
git clone $REPO_URL ~/.termux_doctor

# 5. Alias Setup
if ! grep -q "alias doctor=" ~/.bashrc; then
    echo "alias doctor='python ~/.termux_doctor/core/main.py'" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ Optimization Complete! Type 'doctor' to launch."
