#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: Package Manager Checks

# Load utils (which loads logging + colors)
. "/../lib/utils.sh"

check_packages() {
    log_header

    log_info "Checking if pkg is available..."
    if cmd_exists pkg; then
        log_success "pkg command found."
    else
        log_error "pkg command missing — Termux installation may be corrupted."
        return 1
    fi

    log_info "Checking if apt is available..."
    if cmd_exists apt; then
        log_success "apt command found."
    else
        log_error "apt command missing — severe Termux corruption."
        return 1
    fi

    log_info "Checking package database..."
    if run_safe apt update >/dev/null; then
        log_success "Package database updated successfully."
    else
        log_error "Failed to update package database."
    fi

    log_info "Checking for broken packages..."
    if dpkg --audit | grep -q "packages with problems"; then
        log_warn "Broken packages detected."
        dpkg --audit
    else
        log_success "No broken packages detected."
    fi

    log_info "Checking for available upgrades..."
    upgrades=""
    if [ "" -gt 1 ]; then
        log_warn " packages can be upgraded."
    else
        log_success "All packages are up to date."
    fi

    log_info "Checking core utilities..."
    for cmd in curl wget git tar unzip; do
        if cmd_exists ""; then
            log_success " is installed."
        else
            log_warn " is missing."
        fi
    done

    return 0
}

check_packages
