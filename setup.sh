#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[92m🩺 Termux-Doctor: Scanning System Vitals...\033[0m"

# 1. AUTO-DEPENDENCY INJECTOR
# These are the 'Surgical Tools' needed to build modern Python Metadata
DEPENDENCIES=(clang python-pip libffi openssl rust git)

for pkg in "\"; do
    if ! command -v \ &> /dev/null; then
        echo -e "\033[93m[*] Missing vital component: \. Installing...\033[0m"
        pkg install \ -y
    fi
done

# 2. CORE SYSTEM UPGRADE
echo -e "\033[92m[*] Sanitizing Python Environment...\033[0m"
pip install --upgrade pip
pip install openai

# 3. REPOSITORY RE-SYNC (Underscore Path)
rm -rf ~/.termux_doctor
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor

# 4. WINDOWS-TO-LINUX SANITIZATION
sed -i 's/\r//g' ~/.termux_doctor/core/main.py

# 5. ALIAS LINKING
echo "alias doctor='python ~/.termux_doctor/core/main.py'" > ~/.termux_doctor_alias
sed -i 's/\r//g' ~/.termux_doctor_alias

if ! grep -q "termux_doctor_alias" ~/.bashrc; then
    echo "source ~/.termux_doctor_alias" >> ~/.bashrc
fi

echo -e "\033[92m✅ Environment Sterile. Type 'source ~/.bashrc' then 'doctor'.\033[0m"