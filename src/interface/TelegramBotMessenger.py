import requests

from helper.EnvironmentVars import telegram_url
from interface.NotificationService import NotificationService
from utils.Logger import logger
from exceptions import TelegramBotException

class TelegramBotMessenger(NotificationService):

    def __init__(self, secret):
        self.token = secret["telegram-bot-token"]
        self.chat_id = secret["telegram-chat-id"]

    def send_message(self, message) -> None:
        logger.log("INFO", "Publishing message to the end-user via telegram bot....")

        logger.log("DEBUG", f"Preview message content: {message}")

        # Publish message content with requests
        response = requests.post(
            telegram_url.replace("{token}", self.token),
            json={
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
        )

        if(response.status_code != 200):
            raise TelegramBotException(status_code = response.status_code ,
                                       message = f"Unable to publish message to user. Reason: {response.json}")

