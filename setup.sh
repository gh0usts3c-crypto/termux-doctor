#!/data/data/com.termux/files/usr/bin/bash
echo -e "\033[92m🩺 Installation Finished.\033[0m"
rm -rf ~/.termux_doctor
git clone https://github.com/gh0usts3c-crypto/Termux-Doctor.git ~/.termux_doctor
sed -i 's/\r//g' ~/.termux_doctor/core/main.py
echo "alias doctor='python ~/.termux_doctor/core/main.py'" > ~/.termux_doctor_alias
sed -i 's/\r//g' ~/.termux_doctor_alias
grep -q "termux_doctor_alias" ~/.bashrc || echo "source ~/.termux_doctor_alias" >> ~/.bashrc
echo -e "\033[93mRestart Termux or type 'source ~/.bashrc' then 'doctor' to start.\033[0m"