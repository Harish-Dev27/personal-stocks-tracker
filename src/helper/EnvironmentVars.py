# This file will have all environment vars needed for the application

import os


stocks = os.getenv("STOCKS", "")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
