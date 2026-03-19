#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Utility Library
#  Provides helper functions used across all modules
#=========================================================

# Load color + logging engines
source "$(dirname "$0")/colors.sh"
source "$(dirname "$0")/logging.sh"

#---------------------------------------------------------
# Check if a command exists
# Usage: require_cmd "curl"
#---------------------------------------------------------
require_cmd() {
    local cmd="$1"

    if ! command -v "$cmd" >/dev/null 2>&1; then
        log_error "Missing required command: $cmd"
        return 1
    fi

    return 0
}

#---------------------------------------------------------
# Safe file existence check
# Usage: file_exists "/path/to/file"
#---------------------------------------------------------
file_exists() {
    [[ -f "$1" ]]
}

#---------------------------------------------------------
# Safe directory existence check
# Usage: dir_exists "/path/to/dir"
#---------------------------------------------------------
dir_exists() {
    [[ -d "$1" ]]
}

#---------------------------------------------------------
# Create directory if missing
# Usage: ensure_dir "/path"
#---------------------------------------------------------
ensure_dir() {
    local dir="$1"

    if ! dir_exists "$dir"; then
        mkdir -p "$dir"
        log_info "Created directory: $dir"
    fi
}

#---------------------------------------------------------
# Run a command safely and log output
# Usage: safe_run "apt update"
#---------------------------------------------------------
safe_run() {
    local cmd="$1"

    if eval "$cmd"; then
        log_info "Command succeeded: $cmd"
        return 0
    else
        log_error "Command failed: $cmd"
        return 1
    fi
}

#---------------------------------------------------------
# Read a file safely
# Usage: read_file "/path"
#---------------------------------------------------------
read_file() {
    local file="$1"

    if ! file_exists "$file"; then
        log_error "Cannot read missing file: $file"
        return 1
    fi

    cat "$file"
}

#---------------------------------------------------------
# Write text to a file
# Usage: write_file "/path" "content"
#---------------------------------------------------------
write_file() {
    local file="$1"
    local content="$2"

    echo "$content" > "$file"
    log_info "Wrote to file: $file"
}

# End of file

