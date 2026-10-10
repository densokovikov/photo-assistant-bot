#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
cd "$SCRIPT_DIR"
set -a
source .env
set +a
exec /usr/bin/python3 send_daily.py
