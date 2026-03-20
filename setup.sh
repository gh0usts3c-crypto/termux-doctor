#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Hard-Resetting Termux-Doctor..."

# Remove everything old
rm -rf ~/.termux_doctor
rm -rf ~/.termux_doctor_alias

# Re-clone fresh
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor

# Re-establish Alias
echo "alias doctor='python ~/.termux_doctor/core/main.py'" > ~/.termux_doctor_alias
if ! grep -q "termux_doctor_alias" ~/.bashrc; then
    echo "source ~/.termux_doctor_alias" >> ~/.bashrc
fi
source ~/.bashrc

python ~/.termux_doctor/core/main.py
