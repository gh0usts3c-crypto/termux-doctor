#!/usr/bin/env bash
#=========================================================
#  Termux-Doctor: Environment Diagnostics
#  Checks PATH, shell, variables, and Termux environment
#=========================================================

# Load core libraries
source "$(dirname "$0")/../colors.sh"
source "$(dirname "$0")/../logging.sh"
source "$(dirname "$0")/../utils.sh"
source "$(dirname "$0")/../branding.sh"

#---------------------------------------------------------
# Check Shell Type
#---------------------------------------------------------
check_shell() {
    local shell_name
    shell_name="$SHELL"

    if [[ -z "$shell_name" ]]; then
        warn "Shell variable not set"
        log_warn "Shell variable not set"
    else
        ok "Shell: $shell_name"
        log_info "Shell: $shell_name"
    fi
}

#---------------------------------------------------------
# Check PATH Integrity
#---------------------------------------------------------
check_path() {
    if [[ -z "$PATH" ]]; then
        err "PATH variable is empty!"
        log_error "PATH variable empty"
        return
    fi

    ok "PATH variable detected"
    log_info "PATH: $PATH"

    # Check for Termux PREFIX in PATH
    if [[ "$PATH" == *"$PREFIX"* ]]; then
        ok "PREFIX is present in PATH"
        log_info "PREFIX present in PATH"
    else
        warn "PREFIX missing from PATH"
        log_warn "PREFIX missing from PATH"
    fi
}

#---------------------------------------------------------
# Check Termux Environment Variables
#---------------------------------------------------------
check_termux_env() {
    local vars=("PREFIX" "HOME" "TMPDIR" "LD_LIBRARY_PATH")

    ok "Checking Termux environment variables..."
    for var in "${vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            warn "$var is not set"
            log_warn "$var missing"
        else
            ok "$var = ${!var}"
            log_info "$var = ${!var}"
        fi
    done
}

#---------------------------------------------------------
# Check for Common Misconfigurations
#---------------------------------------------------------
check_common_issues() {
    # ~/.bashrc or ~/.profile corruption
    if file_exists "$HOME/.bashrc"; then
        if grep -q "exit" "$HOME/.bashrc"; then
            warn "~/.bashrc contains 'exit' — may break shell startup"
            log_warn "Suspicious exit in .bashrc"
        fi
    fi

    # Check for broken symlinks in $PREFIX/bin
    local broken
    broken=$(find "$PREFIX/bin" -xtype l 2>/dev/null)

    if [[ -n "$broken" ]]; then
        warn "Broken symlinks detected in \$PREFIX/bin:"
        echo "$broken"
        log_warn "Broken symlinks: $broken"
    else
        ok "No broken symlinks in \$PREFIX/bin"
        log_info "No broken symlinks"
    fi
}

#---------------------------------------------------------
# Run All Environment Checks
#---------------------------------------------------------
run_environment_checks() {
    doctor_banner
    echo -e "${CYAN}Running environment diagnostics...${RESET}"
    echo

    check_shell
    check_path
    check_termux_env
    check_common_issues

    echo
}

