
#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Hybrid Color Engine
#  Provides POSIX-safe ANSI colors with optional neon mode
#=========================================================

#---------------------------------------------------------
# Detect terminal color capability
#---------------------------------------------------------
detect_color_support() {
    # Default to basic ANSI
    COLOR_MODE="basic"

    # Termux supports 256-color and truecolor
    if [[ -n "$TERMUX_VERSION" ]]; then
        COLOR_MODE="neon"
        return
    fi

    # Check COLORTERM for truecolor
    case "$COLORTERM" in
        truecolor|24bit)
            COLOR_MODE="neon"
            ;;
    esac
}

detect_color_support

#---------------------------------------------------------
# Basic ANSI Colors (POSIX-safe)
#---------------------------------------------------------
if [[ "$COLOR_MODE" == "basic" ]]; then
    RED="\033[31m"
    GREEN="\033[32m"
    YELLOW="\033[33m"
    BLUE="\033[34m"
    MAGENTA="\033[35m"
    CYAN="\033[36m"
    WHITE="\033[37m"
    RESET="\033[0m"

    # Status colors
    OK="$GREEN"
    WARN="$YELLOW"
    ERR="$RED"
fi

#---------------------------------------------------------
# Enhanced Neon Mode (Termux / Truecolor)
#---------------------------------------------------------
if [[ "$COLOR_MODE" == "neon" ]]; then
    # Truecolor neon palette
    RED="\033[38;2;255;70;70m"
    GREEN="\033[38;2;80;255;120m"
    YELLOW="\033[38;2;255;220;90m"
    BLUE="\033[38;2;90;170;255m"
    MAGENTA="\033[38;2;255;90;255m"
    CYAN="\033[38;2;90;255;255m"
    WHITE="\033[38;2;240;240;240m"
    RESET="\033[0m"

    # Cyberpunk hazard palette
    OK="\033[38;2;80;255;120m"
    WARN="\033[38;2;255;180;80m"
    ERR="\033[38;2;255;80;120m"
fi

#---------------------------------------------------------
# Utility: colorize text
# Usage: colorize "$RED" "message"
#---------------------------------------------------------
colorize() {
    local color="$1"
    local text="$2"
    echo -e "${color}${text}${RESET}"
}

#---------------------------------------------------------
# Utility: status labels
#---------------------------------------------------------
ok()   { colorize "$OK"   "[OK] $1"; }
warn() { colorize "$WARN" "[WARN] $1"; }
err()  { colorize "$ERR"  "[ERROR] $1"; }

# End of file

