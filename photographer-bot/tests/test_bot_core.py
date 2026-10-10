import unittest

from bot_core import build_daily_message, next_daily_items


class NextDailyItemsTest(unittest.TestCase):
    def test_returns_one_item_and_advances_both_cursors(self):
        photographers = [{"photographer": "A"}, {"photographer": "B"}]
        assignments = [{"assignment": "X"}, {"assignment": "Y"}]

        photographer, assignment, state = next_daily_items(
            photographers,
            assignments,
            {"photographer_index": 0, "assignment_index": 0},
        )

        self.assertEqual(photographer["photographer"], "A")
        self.assertEqual(assignment["assignment"], "X")
        self.assertEqual(state["photographer_index"], 1)
        self.assertEqual(state["assignment_index"], 1)

    def test_wraps_cursors_at_the_end(self):
        photographers = [{"photographer": "A"}, {"photographer": "B"}]
        assignments = [{"assignment": "X"}]

        photographer, assignment, state = next_daily_items(
            photographers,
            assignments,
            {"photographer_index": 1, "assignment_index": 0},
        )

        self.assertEqual(photographer["photographer"], "B")
        self.assertEqual(assignment["assignment"], "X")
        self.assertEqual(state["photographer_index"], 0)
        self.assertEqual(state["assignment_index"], 0)

    def test_rejects_empty_sources(self):
        with self.assertRaisesRegex(ValueError, "photographers"):
            next_daily_items([], [{"assignment": "X"}], {})
        with self.assertRaisesRegex(ValueError, "assignments"):
            next_daily_items([{"photographer": "A"}], [], {})


class BuildDailyMessageTest(unittest.TestCase):
    def test_formats_photographer_and_assignment_and_escapes_html(self):
        photographer = {
            "photographer": "Надар & Co",
            "latin": "Nadar <Studio>",
            "section": "Мастер",
            "topic": "Портрет",
            "style": "Студия",
            "work": "Известная работа",
            "source": "Учебный источник",
            "search_url": "https://example.com/?q=nadar&lang=ru",
        }
        assignment = {
            "part": "Видение и стиль",
            "title": "Диагностика себя",
            "hours": "3 ч",
            "assignment": "Разберите 30 кадров <своих>.",
            "result": "Найдите сильные решения.",
            "course_url": "file:///course.html#t0",
        }

        message = build_daily_message(
            photographer,
            assignment,
            photographer_number=1,
            photographer_total=2,
            assignment_number=1,
            assignment_total=3,
        )

        self.assertIn("Надар &amp; Co", message)
        self.assertIn("Nadar &lt;Studio&gt;", message)
        self.assertIn("Разберите 30 кадров &lt;своих&gt;.", message)
        self.assertIn("Фотограф 1/2", message)
        self.assertIn("Задание 1/3", message)
        self.assertIn('href="https://example.com/?q=nadar&amp;lang=ru"', message)
        self.assertNotIn('href="file:///course.html#t0"', message)


if __name__ == "__main__":
    unittest.main()
