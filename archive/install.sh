#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor Installer
#  Installs the main executable into $PREFIX/bin
#=========================================================

# Load branding + colors for a clean install experience
source "./lib/colors.sh"
source "./lib/branding.sh"

doctor_banner
echo -e "${CYAN}Installing Termux-Doctor...${RESET}"
echo

# Ensure bin directory exists
if [[ ! -d "$PREFIX/bin" ]]; then
    echo -e "${YELLOW}Creating $PREFIX/bin...${RESET}"
    mkdir -p "$PREFIX/bin"
fi

# Copy main executable
echo -e "${CYAN}Copying executable to $PREFIX/bin...${RESET}"
cp ./termux-doctor "$PREFIX/bin/termux-doctor"

# Set permissions
chmod +x "$PREFIX/bin/termux-doctor"

# Verify installation
if command -v termux-doctor >/dev/null 2>&1; then
    echo -e "${GREEN}Installation complete!${RESET}"
    echo -e "${MAGENTA}You can now run:${RESET}"
    echo -e "${CYAN}    termux-doctor${RESET}"
else
    echo -e "${RED}Installation failed â€” termux-doctor not found in PATH.${RESET}"
fi

echo

