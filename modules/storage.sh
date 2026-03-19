#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: Storage Checks

# Load utils (which loads logging + colors)
. "/../lib/utils.sh"

check_storage() {
    log_header

    log_info "Checking internal storage..."
    if dir_exists "C:\Users\gh0us"; then
        log_success "Internal storage OK: C:\Users\gh0us"
    else
        log_error "Internal storage missing: C:\Users\gh0us"
    fi

    log_info "Checking Termux shared storage access..."
    if dir_exists "C:\Users\gh0us/storage"; then
        log_success "Shared storage directory exists."
    else
        log_warn "Shared storage not initialized. Run: termux-setup-storage"
    fi

    log_info "Checking free space..."
    free_space=""
    log_success "Available space: "

    log_info "Checking symlink integrity..."
    if [ -L "C:\Users\gh0us/storage/downloads" ]; then
        log_success "Downloads symlink OK."
    else
        log_warn "Downloads symlink missing or broken."
    fi

    return 0
}

check_storage
