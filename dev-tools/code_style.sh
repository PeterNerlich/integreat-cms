#!/bin/bash

# This script can be used to run both our code style tools black and pylint.

# Import utility functions
# shellcheck source=./dev-tools/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/_functions.sh"

require_installed
ensure_not_root

# Run black
bash "${DEV_TOOL_DIR}/black.sh"

# Run prettier
bash "${DEV_TOOL_DIR}/prettier.sh"

# Run pylint
bash "${DEV_TOOL_DIR}/pylint.sh"
