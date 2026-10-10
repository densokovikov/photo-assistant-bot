import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class TelegramAPI:
    def __init__(self, token):
        token = str(token).strip()
        if not token or ":" not in token:
            raise ValueError("Некорректный токен Telegram")
        self.base_url = f"https://api.telegram.org/bot{token}"

    def _call(self, method, payload, timeout=40):
        request = Request(
            f"{self.base_url}/{method}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            try:
                detail = json.loads(error.read().decode("utf-8")).get("description")
            except Exception:
                detail = None
            raise RuntimeError(detail or f"Telegram вернул HTTP {error.code}") from None
        except URLError as error:
            raise RuntimeError(f"Нет связи с Telegram: {error.reason}") from None
        if not data.get("ok"):
            raise RuntimeError(data.get("description") or "Неизвестная ошибка Telegram")
        return data.get("result")

    def send_message(self, chat_id, text):
        return self._call(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "link_preview_options": {"is_disabled": True},
            },
        )

    def get_updates(self, offset=None, timeout=30):
        payload = {"timeout": timeout, "allowed_updates": ["message"]}
        if offset is not None:
            payload["offset"] = offset
        return self._call("getUpdates", payload, timeout=timeout + 10)
