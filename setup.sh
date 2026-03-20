#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Installing Termux-Doctor..."
pkg update -y && pkg install python git -y
pip install -q -U google-generativeai
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor
echo "alias doctor='python ~/.termux_doctor/core/main.py'" >> ~/.bashrc
echo "✅ Done. Type 'doctor' to start."
