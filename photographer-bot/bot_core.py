from html import escape
from urllib.parse import urlsplit


def next_daily_items(photographers, assignments, state):
    if not photographers:
        raise ValueError("photographers list is empty")
    if not assignments:
        raise ValueError("assignments list is empty")

    photographer_index = int(state.get("photographer_index", 0)) % len(photographers)
    assignment_index = int(state.get("assignment_index", 0)) % len(assignments)
    next_state = dict(state)
    next_state["photographer_index"] = (photographer_index + 1) % len(photographers)
    next_state["assignment_index"] = (assignment_index + 1) % len(assignments)
    return photographers[photographer_index], assignments[assignment_index], next_state


def _line(label, value):
    return f"<b>{escape(label)}:</b> {escape(str(value))}" if value else ""


def _link(label, url):
    if not url:
        return ""
    if urlsplit(str(url)).scheme not in {"http", "https", "tg", "mailto"}:
        return ""
    return f'<a href="{escape(str(url), quote=True)}">{escape(label)}</a>'


def _bullet_list(items):
    return "\n".join(
        f"{index}. {escape(str(item))}" for index, item in enumerate(items or [], start=1)
    )


def build_daily_message(
    photographer,
    assignment,
    *,
    photographer_number,
    photographer_total,
    assignment_number,
    assignment_total,
):
    latin = photographer.get("latin")
    name = f"<b>{escape(str(photographer.get('photographer', 'Без имени')))}</b>"
    if latin:
        name += f"\n<i>{escape(str(latin))}</i>"

    photographer_lines = [
        f"📷 <b>Фотограф {photographer_number}/{photographer_total}</b>",
        name,
        _line("Раздел", photographer.get("section")),
        _line("Тема", photographer.get("topic")),
        _line("Стиль", photographer.get("style")),
        _line("Чем известен", photographer.get("work")),
        _line("Источник", photographer.get("source")),
        _link("Найти работы ↗", photographer.get("search_url")),
    ]

    practice = assignment.get("practice")
    if not practice and assignment.get("assignment"):
        practice = [assignment["assignment"]]
    advice = assignment.get("advice") or []

    assignment_lines = [
        f"📚 <b>Урок {assignment_number}/{assignment_total}</b>",
        f"<b>{escape(str(assignment.get('title', 'Практика')))}</b>",
        _line("Раздел курса", assignment.get("part")),
        _line("Время темы", assignment.get("hours")),
        "\n📖 <b>Теория</b>" if assignment.get("theory") else "",
        escape(str(assignment.get("theory", ""))),
        "\n🎯 <b>Практика</b>" if practice else "",
        _bullet_list(practice),
        "\n✅ <b>Итог</b>" if assignment.get("result") else "",
        escape(str(assignment.get("result", ""))),
        "\n💡 <b>Советы</b>" if advice else "",
        "\n".join(escape(str(item)) for item in advice),
        _line("Источник урока", assignment.get("source")),
        _link("Открыть тему курса ↗", assignment.get("course_url")),
    ]

    photographer_text = "\n".join(line for line in photographer_lines if line)
    assignment_text = "\n".join(line for line in assignment_lines if line)
    return f"{photographer_text}\n\n{assignment_text}"
