import os
import time
from pathlib import Path

from app_io import load_json, save_json
from daily_service import start_chat_from_updates
from telegram_api import TelegramAPI


ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("Нет TELEGRAM_BOT_TOKEN")

    api = TelegramAPI(token)
    state = load_json(STATE_PATH, {"photographer_index": 0, "assignment_index": 0})
    print("Откройте своего бота в Telegram и отправьте ему команду /start")
    print("Ожидаю сообщение до 10 минут…")
    deadline = time.monotonic() + 600
    offset = None
    while time.monotonic() < deadline:
        updates = api.get_updates(offset=offset, timeout=20)
        chat_id, name, next_offset = start_chat_from_updates(updates)
        if next_offset is not None:
            offset = next_offset
        if chat_id:
            state["chat_id"] = chat_id
            state["chat_name"] = name
            save_json(STATE_PATH, state)
            api.send_message(
                chat_id,
                "✅ Бот настроен. Каждый день в 10:00 по Москве я пришлю одного фотографа и одно практическое задание.",
            )
            print(f"Чат зарегистрирован: {name}.")
            return
    raise SystemExit("Не дождался /start. Запустите setup.command ещё раз.")


if __name__ == "__main__":
    main()
