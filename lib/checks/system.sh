#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: System Diagnostics
#  Collects CPU, memory, kernel, and environment details
#=========================================================

# Load core libraries
source "$(dirname "$0")/../colors.sh"
source "$(dirname "$0")/../logging.sh"
source "$(dirname "$0")/../utils.sh"
source "$(dirname "$0")/../branding.sh"

#---------------------------------------------------------
# CPU Information
#---------------------------------------------------------
check_cpu() {
    if file_exists "/proc/cpuinfo"; then
        local cpu
        cpu=$(grep -m1 "model name" /proc/cpuinfo | cut -d: -f2 | xargs)

        if [[ -z "$cpu" ]]; then
            cpu=$(grep -m1 "Hardware" /proc/cpuinfo | cut -d: -f2 | xargs)
        fi

        log_info "CPU: $cpu"
        ok "CPU: $cpu"
    else
        log_warn "Unable to read CPU info"
        warn "CPU info unavailable"
    fi
}

#---------------------------------------------------------
# Memory Information
#---------------------------------------------------------
check_memory() {
    if file_exists "/proc/meminfo"; then
        local mem
        mem=$(grep -m1 "MemTotal" /proc/meminfo | awk '{print $2 " kB"}')

        log_info "Memory: $mem"
        ok "Memory: $mem"
    else
        log_warn "Unable to read memory info"
        warn "Memory info unavailable"
    fi
}

#---------------------------------------------------------
# Kernel Information
#---------------------------------------------------------
check_kernel() {
    local kernel
    kernel=$(uname -r)

    log_info "Kernel: $kernel"
    ok "Kernel: $kernel"
}

#---------------------------------------------------------
# Architecture
#---------------------------------------------------------
check_arch() {
    local arch
    arch=$(uname -m)

    log_info "Architecture: $arch"
    ok "Architecture: $arch"
}

#---------------------------------------------------------
# Android / Termux Version
#---------------------------------------------------------
check_termux_version() {
    if command -v termux-info >/dev/null 2>&1; then
        local version
        version=$(termux-info | grep "Packages CPU architecture" | cut -d: -f2 | xargs)

        log_info "Termux Architecture: $version"
        ok "Termux Architecture: $version"
    else
        warn "termux-info not available"
    fi
}

#---------------------------------------------------------
# Uptime
#---------------------------------------------------------
check_uptime() {
    local up
    up=$(uptime -p 2>/dev/null || echo "Unavailable")

    log_info "Uptime: $up"
    ok "Uptime: $up"
}

#---------------------------------------------------------
# Run All System Checks
#---------------------------------------------------------
run_system_checks() {
    doctor_banner
    echo -e "${CYAN}Running system diagnostics...${RESET}"
    echo

    check_cpu
    check_memory
    check_kernel
    check_arch
    check_termux_version
    check_uptime

    echo
}

