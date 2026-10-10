import json
import unittest
from unittest.mock import patch

from telegram_api import TelegramAPI


class FakeResponse:
    def __init__(self, data):
        self.data = json.dumps(data).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.data


class TelegramAPITest(unittest.TestCase):
    @patch("telegram_api.urlopen")
    def test_send_message_posts_html_payload(self, urlopen):
        urlopen.return_value = FakeResponse({"ok": True, "result": {"message_id": 1}})
        api = TelegramAPI("123:secret")

        result = api.send_message(456, "<b>Привет</b>")

        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["chat_id"], 456)
        self.assertEqual(payload["parse_mode"], "HTML")
        self.assertTrue(payload["link_preview_options"]["is_disabled"])
        self.assertEqual(result["message_id"], 1)

    @patch("telegram_api.urlopen")
    def test_get_updates_passes_offset_and_timeout(self, urlopen):
        urlopen.return_value = FakeResponse({"ok": True, "result": []})
        api = TelegramAPI("123:secret")

        self.assertEqual(api.get_updates(offset=12, timeout=5), [])

        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["offset"], 12)
        self.assertEqual(payload["timeout"], 5)


if __name__ == "__main__":
    unittest.main()
