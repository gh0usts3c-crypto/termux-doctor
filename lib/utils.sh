#!/usr/bin/env bash

require_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This action requires root privileges."
        return 1
    fi
}

check_command() {
    command -v "$1" >/dev/null 2>&1
}

