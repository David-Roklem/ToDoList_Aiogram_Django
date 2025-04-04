from config import settings
import httpx


class Telegram:

    def __init__(self):
        self.url = f"https://api.telegram.org/bot{settings.bot_token}"
        self.transport = httpx.HTTPTransport(retries=3)

    def send_message(self, chat_id: str, text: str):
        endpoint = self.url + "/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        with httpx.Client(transport=self.transport) as client:
            resp = client.post(endpoint, params=params)
            return resp.json()
