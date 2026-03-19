#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: Environment Checks

# Load utils (which loads logging + colors)
. "/../lib/utils.sh"

check_environment() {
    log_header

    log_info "Checking Android version..."
    android_ver=""
    log_success "Android version: "

    log_info "Checking architecture..."
    arch=""
    log_success "Architecture: "

    log_info "Checking shell..."
    log_success "Shell: "

    log_info "Checking PATH..."
    echo "C:\Users\gh0us\Desktop\~termux-doctor" | grep -q "/data/data/com.termux/files/usr/bin"
    if [ False -eq 0 ]; then
        log_success "PATH looks correct."
    else
        log_warn "PATH may be missing Termux bin directory."
    fi

    log_info "Checking Termux directories..."
    for dir in "C:\Users\gh0us" "" "/bin" "/etc"; do
        if dir_exists ""; then
            log_success "Directory exists: "
        else
            log_error "Missing directory: "
        fi
    done

    return 0
}

check_environment
