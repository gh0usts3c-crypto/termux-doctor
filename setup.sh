#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Running Phoenix Reinstall with Debugger..."

export ANDROID_API_LEVEL=26
pkg update -y
pkg install python python-cryptography python-pydantic python-grpcio clang rust git -y

pip install --upgrade pip
pip install google-generativeai --no-build-isolation

rm -rf ~/.termux_doctor
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor

echo "alias doctor='python ~/.termux_doctor/core/main.py'" > ~/.termux_doctor_alias
if ! grep -q "termux_doctor_alias" ~/.bashrc; then
    echo "source ~/.termux_doctor_alias" >> ~/.bashrc
fi
source ~/.bashrc

python ~/.termux_doctor/core/main.py
