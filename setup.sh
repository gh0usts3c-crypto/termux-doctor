#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[92m🩺 Termux-Doctor: Scanning System Vitals...\033[0m"

# 1. AUTO-DEPENDENCY INJECTOR
# Explicitly listing dependencies to avoid loop-syntax failures
pkg update -y
pkg install clang python libffi openssl rust git -y

# 2. CORE SYSTEM UPGRADE
echo -e "\033[92m[*] Sanitizing Python Environment...\033[0m"
pip install --upgrade pip
pip install openai

# 3. REPOSITORY RE-SYNC
rm -rf ~/.termux_doctor
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor

# 4. WINDOWS-TO-LINUX SANITIZATION
# Stripping \r from all core files
find ~/.termux_doctor -type f -name "*.py" -exec sed -i 's/\r//g' {} +
find ~/.termux_doctor -type f -name "*.sh" -exec sed -i 's/\r//g' {} +

# 5. ALIAS LINKING
# Using a safer heredoc for the alias file
cat <<EOF > ~/.termux_doctor_alias
alias doctor='python ~/.termux_doctor/core/main.py'
EOF

sed -i 's/\r//g' ~/.termux_doctor_alias

if ! grep -q "termux_doctor_alias" ~/.bashrc; then
    echo "source ~/.termux_doctor_alias" >> ~/.bashrc
fi

echo -e "\033[92m✅ Environment Sterile. Restart Termux or type 'source ~/.bashrc' then 'doctor'.\033[0m"