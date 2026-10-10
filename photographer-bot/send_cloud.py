import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app_io import load_json
from cloud_service import prepare_cloud_delivery
from telegram_api import TelegramAPI


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Europe/Moscow")


def required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"GitHub secret {name} is not configured")
    return value


def main():
    token = required_env("TELEGRAM_BOT_TOKEN")
    chat_id = required_env("TELEGRAM_CHAT_ID")
    start_date = date.fromisoformat(os.environ.get("CLOUD_START_DATE", "2026-10-10"))
    today = datetime.now(TIMEZONE).date()
    photographers = load_json(ROOT / "data" / "photographers.json", [])
    assignments = load_json(ROOT / "data" / "assignments.json", [])
    message = prepare_cloud_delivery(
        photographers,
        assignments,
        start_date=start_date,
        today=today,
        photographer_start_index=int(os.environ.get("PHOTOGRAPHER_START_INDEX", "0")),
        assignment_start_index=int(os.environ.get("ASSIGNMENT_START_INDEX", "0")),
    )
    TelegramAPI(token).send_message(chat_id, message)
    print(f"Daily message sent for {today.isoformat()}.")


if __name__ == "__main__":
    main()
