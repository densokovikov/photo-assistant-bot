import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app_io import load_json, save_json
from daily_service import prepare_daily_delivery, should_send_today
from telegram_api import TelegramAPI


ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"
PHOTOGRAPHERS_PATH = ROOT / "data" / "photographers.json"
ASSIGNMENTS_PATH = ROOT / "data" / "assignments.json"
TIMEZONE = ZoneInfo("Europe/Moscow")


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("Нет TELEGRAM_BOT_TOKEN. Сначала запустите setup.command")

    state = load_json(STATE_PATH, {"photographer_index": 0, "assignment_index": 0})
    now = datetime.now(TIMEZONE)
    force = os.environ.get("FORCE_SEND") == "1"
    if not should_send_today(state, now.date(), force=force):
        print("Сегодняшнее сообщение уже отправлено.")
        return

    photographers = load_json(PHOTOGRAPHERS_PATH, [])
    assignments = load_json(ASSIGNMENTS_PATH, [])
    chat_id, message, next_state = prepare_daily_delivery(
        photographers, assignments, state
    )
    TelegramAPI(token).send_message(chat_id, message)
    next_state["last_sent_date"] = now.date().isoformat()
    next_state["last_sent_at"] = now.isoformat()
    save_json(STATE_PATH, next_state)
    print("Сообщение отправлено.")


if __name__ == "__main__":
    main()
