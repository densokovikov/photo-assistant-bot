import re
import unittest
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github"
    / "workflows"
    / "daily-telegram.yml"
)


class DailyWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_has_primary_and_backup_moscow_schedules(self):
        cron_values = re.findall(r'cron:\s*["\']([^"\']+)', self.workflow)

        self.assertIn("0 10 * * *", cron_values)
        self.assertIn("17 10-23 * * *", cron_values)
        self.assertGreaterEqual(
            self.workflow.count('timezone: "Europe/Moscow"'), 2
        )

    def test_skips_delivery_after_today_was_sent(self):
        self.assertIn("actions/cache/restore@v4", self.workflow)
        self.assertIn("telegram-delivery-${{ env.DELIVERY_DATE }}", self.workflow)
        self.assertIn("steps.delivery-cache.outputs.cache-hit != 'true'", self.workflow)
        self.assertIn("actions/cache/save@v4", self.workflow)


if __name__ == "__main__":
    unittest.main()
