#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Patching Doctor Namespace..."

# 1. Install the missing base 'google' module
pkg install python-cryptography python-pydantic python-grpcio -y
pip install --upgrade pip
pip install google-api-core
pip install google-generativeai --no-build-isolation

# 2. Force a refresh of the local python path
export PYTHONPATH=$PYTHONPATH:.

# 3. Run the tool
python ~/.termux_doctor/core/main.py
