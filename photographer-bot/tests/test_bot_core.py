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
            "theory": "Сначала изучите <свои> повторяющиеся решения.",
            "practice": [
                "Разберите 30 кадров <своих>.",
                "Соберите короткую серию.",
            ],
            "result": "Найдите сильные решения.",
            "advice": [
                "Начните с одной темы.",
                "Проверьте выводы на новой съёмке.",
            ],
            "source": "Учебный материал курса.",
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
        self.assertIn("Урок 1/3", message)
        self.assertIn("Теория", message)
        self.assertIn("Сначала изучите &lt;свои&gt; повторяющиеся решения.", message)
        self.assertIn("Практика", message)
        self.assertIn("Разберите 30 кадров &lt;своих&gt;.", message)
        self.assertIn("Соберите короткую серию.", message)
        self.assertIn("Начните с одной темы.", message)
        self.assertIn("Проверьте выводы на новой съёмке.", message)
        self.assertIn("Учебный материал курса.", message)
        self.assertIn("Фотограф 1/2", message)
        self.assertIn('href="https://example.com/?q=nadar&amp;lang=ru"', message)
        self.assertNotIn('href="file:///course.html#t0"', message)


if __name__ == "__main__":
    unittest.main()
