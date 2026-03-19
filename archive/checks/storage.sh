#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Storage Diagnostics
#  Checks disk usage, storage permissions, and directories
#=========================================================

# Load core libraries
source "$(dirname "$0")/../colors.sh"
source "$(dirname "$0")/../logging.sh"
source "$(dirname "$0")/../utils.sh"
source "$(dirname "$0")/../branding.sh"

#---------------------------------------------------------
# Check Termux Storage Permissions
#---------------------------------------------------------
check_storage_permission() {
    if [[ -d "$HOME/storage" ]]; then
        ok "Termux storage permission granted"
        log_info "Termux storage permission granted"
    else
        warn "Termux storage not initialized"
        log_warn "Termux storage not initialized"
        warn "Run: termux-setup-storage"
    fi
}

#---------------------------------------------------------
# Check Internal Storage Usage
#---------------------------------------------------------
check_internal_storage() {
    local usage
    usage=$(df -h / | awk 'NR==2 {print $3 " used / " $2 " total (" $5 ")"}')

    ok "Internal Storage: $usage"
    log_info "Internal Storage: $usage"
}

#---------------------------------------------------------
# Check Home Directory Size
#---------------------------------------------------------
check_home_size() {
    if dir_exists "$HOME"; then
        local size
        size=$(du -sh "$HOME" 2>/dev/null | awk '{print $1}')

        ok "Home Directory Size: $size"
        log_info "Home Directory Size: $size"
    else
        err "Home directory missing!"
        log_error "Home directory missing!"
    fi
}

#---------------------------------------------------------
# Check External / SD Card Storage
#---------------------------------------------------------
check_external_storage() {
    local sdcard="/storage/emulated/0"

    if dir_exists "$sdcard"; then
        local size
        size=$(df -h "$sdcard" | awk 'NR==2 {print $3 " used / " $2 " total (" $5 ")"}')

        ok "External Storage: $size"
        log_info "External Storage: $size"
    else
        warn "External storage not detected"
        log_warn "External storage not detected"
    fi
}

#---------------------------------------------------------
# Run All Storage Checks
#---------------------------------------------------------
run_storage_checks() {
    doctor_banner
    echo -e "${CYAN}Running storage diagnostics...${RESET}"
    echo

    check_storage_permission
    check_internal_storage
    check_home_size
    check_external_storage

    echo
}

