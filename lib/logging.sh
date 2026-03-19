#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Logging Engine
#  Provides timestamped, colorized, and file-based logging
#=========================================================

# Load color engine
source "$(dirname "$0")/colors.sh"

#---------------------------------------------------------
# Log file location
#---------------------------------------------------------
LOG_DIR="$HOME/.termux-doctor/logs"
LOG_FILE="$LOG_DIR/doctor.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

#---------------------------------------------------------
# Timestamp generator
#---------------------------------------------------------
timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

#---------------------------------------------------------
# Core logger
# Usage: log "LEVEL" "message"
#---------------------------------------------------------
log() {
    local level="$1"
    local message="$2"
    local ts
    ts="$(timestamp)"

    echo "[$ts] [$level] $message" >> "$LOG_FILE"
}

#---------------------------------------------------------
# Public logging functions
#---------------------------------------------------------
log_info() {
    log "INFO" "$1"
    ok "$1"
}

log_warn() {
    log "WARN" "$1"
    warn "$1"
}

log_error() {
    log "ERROR" "$1"
    err "$1"
}

# End of file
