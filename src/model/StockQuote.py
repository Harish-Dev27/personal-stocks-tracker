from dataclasses import dataclass
from datetime import datetime


@dataclass
class StockQuote:
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float