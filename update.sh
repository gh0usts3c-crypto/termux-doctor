
#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor Updater
#  Pulls the latest version from GitHub and reinstalls
#=========================================================

# Load branding + colors
source "./lib/colors.sh"
source "./lib/branding.sh"

doctor_banner
echo -e "${CYAN}Checking for updates...${RESET}"
echo

#---------------------------------------------------------
# GitHub Repository (CHANGE THIS TO YOUR REAL REPO)
#---------------------------------------------------------
REPO_URL="https://github.com/Xntoxicated/termux-doctor.git"
TMP_DIR="$HOME/.termux-doctor-update"

#---------------------------------------------------------
# Ensure git exists
#---------------------------------------------------------
if ! command -v git >/dev/null 2>&1; then
    echo -e "${RED}Git is not installed. Cannot update.${RESET}"
    exit 1
fi

#---------------------------------------------------------
# Prepare temporary directory
#---------------------------------------------------------
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo -e "${CYAN}Downloading latest version...${RESET}"

if git clone --depth 1 "$REPO_URL" "$TMP_DIR" >/dev/null 2>&1; then
    echo -e "${GREEN}Download complete.${RESET}"
else
    echo -e "${RED}Failed to download update. Check your internet connection.${RESET}"
    exit 1
fi

#---------------------------------------------------------
# Install updated executable
#---------------------------------------------------------
echo -e "${CYAN}Updating global installation...${RESET}"

cp "$TMP_DIR/termux-doctor" "$PREFIX/bin/termux-doctor"
chmod +x "$PREFIX/bin/termux-doctor"

#---------------------------------------------------------
# Cleanup
#---------------------------------------------------------
rm -rf "$TMP_DIR"

#---------------------------------------------------------
# Verify update
#---------------------------------------------------------
if command -v termux-doctor >/dev/null 2>&1; then
    echo -e "${GREEN}Update successful!${RESET}"
    echo -e "${MAGENTA}Run:${RESET}"
    echo -e "${CYAN}    termux-doctor${RESET}"
else
    echo -e "${RED}Update failed — executable missing.${RESET}"
fi

echo


