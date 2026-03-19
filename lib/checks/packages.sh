#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Package Diagnostics
#  Checks apt health, broken packages, and updates
#=========================================================

# Load core libraries
source "$(dirname "$0")/../colors.sh"
source "$(dirname "$0")/../logging.sh"
source "$(dirname "$0")/../utils.sh"
source "$(dirname "$0")/../branding.sh"

#---------------------------------------------------------
# Check for Broken Packages
#---------------------------------------------------------
check_broken_packages() {
    if require_cmd dpkg; then
        local broken
        broken=$(dpkg --audit 2>/dev/null)

        if [[ -z "$broken" ]]; then
            ok "No broken packages detected"
            log_info "No broken packages detected"
        else
            err "Broken packages found:"
            echo "$broken"
            log_error "Broken packages: $broken"
        fi
    else
        warn "dpkg not available — cannot check broken packages"
    fi
}

#---------------------------------------------------------
# Check for Available Updates
#---------------------------------------------------------
check_updates() {
    if require_cmd apt; then
        local updates
        updates=$(apt list --upgradeable 2>/dev/null | grep -v "Listing..." )

        if [[ -z "$updates" ]]; then
            ok "All packages are up to date"
            log_info "No updates available"
        else
            warn "Updates available:"
            echo "$updates"
            log_warn "Updates available: $updates"
        fi
    else
        warn "apt not available — skipping update check"
    fi
}

#---------------------------------------------------------
# Check APT Database Health
#---------------------------------------------------------
check_apt_health() {
    if require_cmd apt; then
        if apt update >/dev/null 2>&1; then
            ok "APT database is healthy"
            log_info "APT database OK"
        else
            err "APT database update failed"
            log_error "APT database update failed"
        fi
    else
        warn "apt not available — cannot check database health"
    fi
}

#---------------------------------------------------------
# Check Essential Packages
#---------------------------------------------------------
check_essential_packages() {
    local essentials=("curl" "wget" "git" "tar" "proot" "python")

    ok "Checking essential packages..."
    for pkg in "${essentials[@]}"; do
        if command -v "$pkg" >/dev/null 2>&1; then
            ok "$pkg installed"
            log_info "$pkg installed"
        else
            warn "$pkg missing"
            log_warn "$pkg missing"
        fi
    done
}

#---------------------------------------------------------
# Run All Package Checks
#---------------------------------------------------------
run_package_checks() {
    doctor_banner
    echo -e "${CYAN}Running package diagnostics...${RESET}"
    echo

    check_broken_packages
    check_updates
    check_apt_health
    check_essential_packages

    echo
}

