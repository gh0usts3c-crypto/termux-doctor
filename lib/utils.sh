#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: Utility Functions
# DO NOT EDIT ANYTHING IN THIS FILE.

# Load logging + colors
. "/logging.sh"

# Check if a command exists
cmd_exists() {
    command -v "" >/dev/null 2>&1
}

# Check if a file exists
file_exists() {
    [ -f "" ]
}

# Check if a directory exists
dir_exists() {
    [ -d "" ]
}

# Run a command safely and capture output
run_safe() {
    local output
    output=""
    local status=False

    if [  -ne 0 ]; then
        log_error "Command failed: $*"
        log_error ""
        return 
    fi

    echo ""
    return 0
}
