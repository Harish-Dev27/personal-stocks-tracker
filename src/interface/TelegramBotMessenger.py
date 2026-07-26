from interface.NotificationService import NotificationService
from helper.EnvironmentVars import telegram_url
from utils.Logger import logger
import requests

class TelegramBotMessenger(NotificationService):

    def __init__(self, secret):
        self.token = secret["telegram-bot-token"]
        self.chat_id = secret["telegram-chat-id"]

    def send_message(self, message) -> None:
        logger.log("INFO", "Publishing message to the end-user via telegram bot....")

        logger.log("DEBUG", f"Preview message content: {message}")

        try:
            requests.post(
                telegram_url.replace("{token}", self.token),
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
            )
        except Exception as e:
            logger.log("ERROR", f"Unable to publish message to the bot. Reason:{e}")