# This file will have all environment vars needed for the application

import os


stocks = os.getenv("STOCKS", "")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
app_secret_name = os.getenv("APP_SECRET_NAME", "app-secret")
ai_model = os.getenv("AI_MODEL", "gpt-5-mini")
telegram_url = os.getenv("BOT_URL", "https://api.telegram.org/bot{token}/sendMessage")
