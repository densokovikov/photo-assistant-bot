#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
cd "$SCRIPT_DIR"

echo "Настройка Telegram-бота"
echo "Вставьте НОВЫЙ токен от BotFather. Ввод не будет виден:"
read -rs TELEGRAM_BOT_TOKEN
echo

if [[ ! "$TELEGRAM_BOT_TOKEN" =~ '^[0-9]+:[A-Za-z0-9_-]+$' ]]; then
  echo "Токен выглядит некорректно. Запустите файл ещё раз."
  read "REPLY?Нажмите Enter, чтобы закрыть окно…"
  exit 1
fi

umask 077
print -r -- "TELEGRAM_BOT_TOKEN='$TELEGRAM_BOT_TOKEN'" > .env
export TELEGRAM_BOT_TOKEN

/usr/bin/python3 register_chat.py

PLIST_SOURCE="$SCRIPT_DIR/com.photoassistant.daily.plist"
PLIST_TARGET="$HOME/Library/LaunchAgents/com.photoassistant.daily.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$SCRIPT_DIR/logs"
cp "$PLIST_SOURCE" "$PLIST_TARGET"
/bin/launchctl bootout "gui/$UID" "$PLIST_TARGET" >/dev/null 2>&1 || true
/bin/launchctl bootstrap "gui/$UID" "$PLIST_TARGET"
/bin/launchctl enable "gui/$UID/com.photoassistant.daily"

echo
echo "Готово: ежедневная отправка настроена на 10:00 по Москве."
echo "Чтобы проверить прямо сейчас, дважды нажмите send-now.command."
read "REPLY?Нажмите Enter, чтобы закрыть окно…"
