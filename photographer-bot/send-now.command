#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
cd "$SCRIPT_DIR"
set -a
source .env
set +a
FORCE_SEND=1 /usr/bin/python3 send_daily.py
echo
read "REPLY?Нажмите Enter, чтобы закрыть окно…"
