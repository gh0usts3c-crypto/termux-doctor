#!/data/data/com.termux/files/usr/bin/bash
# Termux-Doctor: Network Checks

# Load utils (which loads logging + colors)
. "/../lib/utils.sh"

check_network() {
    log_header

    log_info "Checking internet connectivity..."
    if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
        log_success "Internet reachable (ICMP)."
    else
        log_error "No internet connectivity (ICMP failed)."
    fi

    log_info "Checking DNS resolution..."
    if nslookup google.com >/dev/null 2>&1; then
        log_success "DNS resolution OK."
    else
        log_warn "DNS resolution failed."
    fi

    log_info "Checking IPv4..."
    if ip -4 addr show | grep -q "inet "; then
        log_success "IPv4 address detected."
    else
        log_warn "No IPv4 address detected."
    fi

    log_info "Checking IPv6..."
    if ip -6 addr show | grep -q "inet6 "; then
        log_success "IPv6 address detected."
    else
        log_warn "No IPv6 address detected."
    fi

    log_info "Checking Termux package repo reachability..."
    if curl -s https://packages.termux.dev >/dev/null; then
        log_success "Termux repo reachable."
    else
        log_warn "Termux repo unreachable."
    fi

    return 0
}

check_network
