import unittest
from datetime import date

from daily_service import prepare_daily_delivery, should_send_today, start_chat_from_updates


class PrepareDailyDeliveryTest(unittest.TestCase):
    def test_prepares_message_and_next_state_without_mutating_current_state(self):
        photographers = [
            {
                "photographer": "Надар",
                "section": "Мастер",
                "topic": "Портрет",
                "work": "Портреты",
            }
        ]
        assignments = [
            {
                "part": "Техника",
                "title": "Оптика",
                "assignment": "Снимите три кадра.",
                "result": "Сравните перспективу.",
            }
        ]
        state = {"chat_id": 123, "photographer_index": 0, "assignment_index": 0}

        chat_id, message, next_state = prepare_daily_delivery(
            photographers, assignments, state
        )

        self.assertEqual(chat_id, 123)
        self.assertIn("Надар", message)
        self.assertIn("Снимите три кадра.", message)
        self.assertEqual(state["photographer_index"], 0)
        self.assertEqual(next_state["photographer_index"], 0)

    def test_requires_registered_chat(self):
        with self.assertRaisesRegex(ValueError, "/start"):
            prepare_daily_delivery([{"photographer": "A"}], [{"assignment": "X"}], {})


class StartChatFromUpdatesTest(unittest.TestCase):
    def test_finds_private_start_command(self):
        updates = [
            {"update_id": 10, "message": {"chat": {"id": -1, "type": "group"}, "text": "/start"}},
            {
                "update_id": 11,
                "message": {
                    "chat": {"id": 456, "type": "private", "first_name": "Денис"},
                    "text": "/start payload",
                },
            },
        ]

        self.assertEqual(start_chat_from_updates(updates), (456, "Денис", 12))

    def test_returns_next_offset_when_start_is_absent(self):
        updates = [{"update_id": 20, "message": {"chat": {"id": 1}, "text": "привет"}}]

        self.assertEqual(start_chat_from_updates(updates), (None, None, 21))


class ShouldSendTodayTest(unittest.TestCase):
    def test_skips_a_second_scheduled_delivery_on_the_same_day(self):
        state = {"last_sent_date": "2026-10-10"}

        self.assertFalse(should_send_today(state, date(2026, 10, 10)))
        self.assertTrue(should_send_today(state, date(2026, 10, 11)))

    def test_force_allows_manual_test_delivery(self):
        state = {"last_sent_date": "2026-10-10"}

        self.assertTrue(should_send_today(state, date(2026, 10, 10), force=True))


if __name__ == "__main__":
    unittest.main()
