from bot_core import build_daily_message, next_daily_items


def should_send_today(state, today, force=False):
    return force or state.get("last_sent_date") != today.isoformat()


def prepare_daily_delivery(photographers, assignments, state):
    chat_id = state.get("chat_id")
    if not chat_id:
        raise ValueError("Чат не зарегистрирован: отправьте боту /start")

    photographer_index = int(state.get("photographer_index", 0)) % len(photographers)
    assignment_index = int(state.get("assignment_index", 0)) % len(assignments)
    photographer, assignment, next_state = next_daily_items(
        photographers, assignments, state
    )
    message = build_daily_message(
        photographer,
        assignment,
        photographer_number=photographer_index + 1,
        photographer_total=len(photographers),
        assignment_number=assignment_index + 1,
        assignment_total=len(assignments),
    )
    return chat_id, message, next_state


def start_chat_from_updates(updates):
    offset = None
    for update in updates:
        update_id = int(update.get("update_id", 0))
        offset = max(offset or 0, update_id + 1)
        message = update.get("message") or {}
        chat = message.get("chat") or {}
        text = str(message.get("text", "")).strip()
        if chat.get("type") == "private" and text.split(maxsplit=1)[0] == "/start":
            name = chat.get("first_name") or chat.get("username") or "пользователь"
            return chat.get("id"), name, offset
    return None, None, offset
