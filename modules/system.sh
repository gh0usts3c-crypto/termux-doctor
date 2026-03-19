#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: System Information Checks

# Load utils (which loads logging + colors)
. "/../lib/utils.sh"

check_system() {
    log_header

    log_info "Checking kernel version..."
    kernel=""
    log_success "Kernel: "

    log_info "Checking device model..."
    model=""
    log_success "Device model: "

    log_info "Checking manufacturer..."
    manufacturer=""
    log_success "Manufacturer: "

    log_info "Checking uptime..."
    uptime_val=""
    log_success "Uptime: "

    log_info "Checking CPU info..."
    cpu=""
    if [ -n "" ]; then
        log_success "CPU: "
    else
        log_warn "CPU info not available."
    fi

    log_info "Checking memory..."
    mem_total=""
    mem_free=""
    log_success "Memory total: kB"
    log_success "Memory available: kB"

    log_info "Checking SELinux mode..."
    selinux=""
    if [ -n "" ]; then
        log_success "SELinux: "
    else
        log_warn "SELinux not available."
    fi

    log_info "Checking Termux app version..."
    termux_ver=""
    if [ -n "" ]; then
        log_success "Termux version: "
    else
        log_warn "Termux version not available."
    fi

    return 0
}

check_system
