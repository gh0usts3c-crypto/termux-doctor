#!/data/data/com.termux/files/usr/bin/bash
echo "🩺 Building Isolated Diagnostic Environment..."

# 1. Purge old broken links
rm -rf ~/.termux_doctor
pkg update -y
pkg install python git clang rust binutils -y

# 2. Clone the Repository
REPO_URL="https://github.com/gh0usts3c-crypto/Termux-Doctor.git"
git clone $REPO_URL ~/.termux_doctor
cd ~/.termux_doctor

# 3. Create the Virtual Environment (The Clean Room)
python -m venv venv
source venv/bin/activate

# 4. Install dependencies INSIDE the venv (No build isolation here)
pip install --upgrade pip setuptools wheel
echo "📦 Installing AI Core into isolated container..."
pip install google-generativeai

# 5. Create a Wrapper Script for the Alias
echo "#!/data/data/com.termux/files/usr/bin/bash" > doctor_run.sh
echo "source ~/.termux_doctor/venv/bin/activate" >> doctor_run.sh
echo "python ~/.termux_doctor/core/main.py \"\$@\"" >> doctor_run.sh
chmod +x doctor_run.sh

# 6. Global Alias Setup
if ! grep -q "alias doctor=" ~/.bashrc; then
    echo "alias doctor='~/.termux_doctor/doctor_run.sh'" >> ~/.bashrc
fi
source ~/.bashrc

echo "✅ VENV DEPLOYMENT COMPLETE! Type 'doctor'."
