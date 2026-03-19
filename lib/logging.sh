#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: Logging Utilities
# DO NOT EDIT ANYTHING IN THIS FILE EXCEPT THE HEADER TEXT BELOW.

# ===== HEADER TEXT (SAFE TO EDIT LATER) =====
HEADER_TEXT="Termux Doctor"
# ============================================

# Load colors
. "/colors.sh"

log_info() {
    echo -e "[INFO] "
}

log_success() {
    echo -e "[OK] "
}

log_warn() {
    echo -e "[WARN] "
}

log_error() {
    echo -e "[ERROR] "
}

log_recommend() {
    echo -e "[RECOMMEND] "
}

log_header() {
    echo -e "===  ==="
}
