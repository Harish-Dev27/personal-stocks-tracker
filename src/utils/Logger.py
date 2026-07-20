from __future__ import annotations

from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from aws_lambda_powertools import Logger as PowertoolsLogger


class Logger:
    _instance: Optional["Logger"] = None

    def __new__(cls, *args, **kwargs) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, service: str = "personal-stocks-tracker") -> None:
        if getattr(self, "_initialized", False):
            return

        self._logger = PowertoolsLogger(service=service)
        
        now = datetime.now(ZoneInfo("Asia/Kolkata"))
        self.timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")

        self._logger.append_keys(timestamp=self.timestamp)
        self._initialized = True

    def log(self, log_type: str, msg: str) -> None:
        level = log_type.upper()
        if level == "INFO":
            self._logger.info(msg)
        elif level == "ERROR":
            self._logger.error(msg)
        elif level == "WARN" or level == "WARNING":
            self._logger.warning(msg)
        elif level == "DEBUG":
            self._logger.debug(msg)
        else:
            self._logger.info(msg)


logger = Logger(service="personal-stocks-tracker")
