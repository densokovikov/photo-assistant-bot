from bot_core import build_daily_message


def daily_index(start_date, today, start_index, total):
    if total <= 0:
        raise ValueError("daily sequence is empty")
    elapsed_days = (today - start_date).days
    if elapsed_days < 0:
        raise ValueError("today is before cloud start date")
    return (int(start_index) + elapsed_days) % total


def prepare_cloud_delivery(
    photographers,
    assignments,
    *,
    start_date,
    today,
    photographer_start_index=0,
    assignment_start_index=0,
):
    photographer_index = daily_index(
        start_date, today, photographer_start_index, len(photographers)
    )
    assignment_index = daily_index(
        start_date, today, assignment_start_index, len(assignments)
    )
    return build_daily_message(
        photographers[photographer_index],
        assignments[assignment_index],
        photographer_number=photographer_index + 1,
        photographer_total=len(photographers),
        assignment_number=assignment_index + 1,
        assignment_total=len(assignments),
    )
