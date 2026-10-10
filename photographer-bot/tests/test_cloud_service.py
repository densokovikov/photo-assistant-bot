import unittest
from datetime import date

from cloud_service import daily_index, prepare_cloud_delivery


class DailyIndexTest(unittest.TestCase):
    def test_advances_once_per_moscow_calendar_day(self):
        start = date(2026, 10, 10)

        self.assertEqual(daily_index(start, date(2026, 10, 10), 0, 341), 0)
        self.assertEqual(daily_index(start, date(2026, 10, 11), 0, 341), 1)
        self.assertEqual(daily_index(start, date(2026, 10, 12), 340, 341), 1)

    def test_rejects_dates_before_cloud_start(self):
        with self.assertRaisesRegex(ValueError, "start date"):
            daily_index(date(2026, 10, 10), date(2026, 10, 9), 0, 10)


class PrepareCloudDeliveryTest(unittest.TestCase):
    def test_uses_date_for_both_sequences(self):
        photographers = [{"photographer": "A"}, {"photographer": "B"}]
        assignments = [{"assignment": "X"}, {"assignment": "Y"}, {"assignment": "Z"}]

        message = prepare_cloud_delivery(
            photographers,
            assignments,
            start_date=date(2026, 10, 10),
            today=date(2026, 10, 11),
            photographer_start_index=0,
            assignment_start_index=0,
        )

        self.assertIn("B", message)
        self.assertIn("Y", message)
        self.assertIn("Фотограф 2/2", message)
        self.assertIn("Задание 2/3", message)


if __name__ == "__main__":
    unittest.main()
