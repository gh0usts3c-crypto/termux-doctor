#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[92m🩺 Termux-Doctor: Injecting System Stability Headers...\033[0m"

# 1. FIX ANDROID_API_LEVEL (Resolves the Jitter/Metadata issue)
export ANDROID_API_LEVEL=34
if ! grep -q "ANDROID_API_LEVEL" ~/.bashrc; then
    echo "export ANDROID_API_LEVEL=34" >> ~/.bashrc
fi

# 2. INSTALL COMPILERS & HEADERS
pkg update -y
pkg install clang python libffi openssl rust git binutils -y

# 3. CLEAN INSTALL OPENAI
pip install --upgrade pip
pip install openai

# 4. RE-SYNC REPOSITORY
rm -rf ~/.termux_doctor
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor

# 5. ALIAS WITH ENVIRONMENT INJECTION
# We wrap the python command with the API LEVEL to ensure it never jitters
cat <<EOF > ~/.termux_doctor_alias
alias doctor='export ANDROID_API_LEVEL=34 && python ~/.termux_doctor/core/main.py'
EOF

find ~/.termux_doctor -type f -name "*.py" -exec sed -i 's/\r//g' {} +
source ~/.bashrc

echo -e "\033[92m✅ Jitter Resolved. Type 'doctor' to begin.\033[0m"