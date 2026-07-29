
class TelegramBotException(Exception):
    """Custom exception for Telegram bot failures."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.message} (status_code={self.status_code})"