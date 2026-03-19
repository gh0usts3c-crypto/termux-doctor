#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Network Diagnostics
#  Tests connectivity, DNS, latency, and IP information
#=========================================================

# Load core libraries
source "$(dirname "$0")/../colors.sh"
source "$(dirname "$0")/../logging.sh"
source "$(dirname "$0")/../utils.sh"
source "$(dirname "$0")/../branding.sh"

#---------------------------------------------------------
# Check Local IP Address
#---------------------------------------------------------
check_local_ip() {
    local ip
    ip=$(ip addr show wlan0 2>/dev/null | grep "inet " | awk '{print $2}' | cut -d/ -f1)

    if [[ -z "$ip" ]]; then
        warn "Local IP not detected"
        log_warn "Local IP not detected"
    else
        ok "Local IP: $ip"
        log_info "Local IP: $ip"
    fi
}

#---------------------------------------------------------
# Check Public IP Address
#---------------------------------------------------------
check_public_ip() {
    if require_cmd curl; then
        local pip
        pip=$(curl -s https://api.ipify.org)

        if [[ -z "$pip" ]]; then
            warn "Public IP unavailable"
            log_warn "Public IP unavailable"
        else
            ok "Public IP: $pip"
            log_info "Public IP: $pip"
        fi
    else
        warn "curl not installed — skipping public IP check"
    fi
}

#---------------------------------------------------------
# Ping Test (Google DNS)
#---------------------------------------------------------
check_ping() {
    if require_cmd ping; then
        if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
            ok "Ping: Online (8.8.8.8 reachable)"
            log_info "Ping successful"
        else
            err "Ping: Offline (8.8.8.8 unreachable)"
            log_error "Ping failed"
        fi
    else
        warn "ping command not available"
    fi
}

#---------------------------------------------------------
# DNS Resolution Test
#---------------------------------------------------------
check_dns() {
    if getent hosts google.com >/dev/null 2>&1; then
        ok "DNS: Resolution working"
        log_info "DNS resolution working"
    else
        err "DNS: Resolution failed"
        log_error "DNS resolution failed"
    fi
}

#---------------------------------------------------------
# Network Interface Summary
#---------------------------------------------------------
check_interfaces() {
    if require_cmd ip; then
        local interfaces
        interfaces=$(ip -o link show | awk -F': ' '{print $2}')

        ok "Interfaces detected:"
        echo "$interfaces"
        log_info "Interfaces: $interfaces"
    else
        warn "ip command not available"
    fi
}

#---------------------------------------------------------
# Run All Network Checks
#---------------------------------------------------------
run_network_checks() {
    doctor_banner
    echo -e "${CYAN}Running network diagnostics...${RESET}"
    echo

    check_local_ip
    check_public_ip
    check_ping
    check_dns
    check_interfaces

    echo
}

