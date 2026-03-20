#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Starting Termux-Doctor Installation..."

# A. Update System and Install Pre-compiled Binaries
# We install python-cryptography via 'pkg' to skip the broken 'pip' build
pkg update -y && pkg upgrade -y
pkg install python python-cryptography clang rust binutils git termux-api -y

# B. Prepare Python Environment
pip install --upgrade pip setuptools wheel
echo "📦 Installing AI Core (this may take a minute)..."
pip install google-generativeai

# C. Clone/Update the Repository
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
rm -rf ~/.termux_doctor
git clone $REPO_URL ~/.termux_doctor

# D. Finalize Environment
if ! grep -q "alias doctor=" ~/.bashrc; then
    echo "alias doctor='python ~/.termux_doctor/core/main.py'" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ Termux-Doctor is ready! Type 'doctor' to launch."
