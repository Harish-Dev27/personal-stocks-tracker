import yfinance as yf
import pandas as pd
from utils.Logger import logger
from model import StockQuote

class StocksInfo:

    def __init__(self, stocks):
        self.stocks = stocks.strip().split(",") #list of stocks whose info needs to be extracted


    """
    First get the stock prices form the Yahoo Finance
    and then populate it into a list
    """
    def get_stocks_latest_price(self):
        try:
            stock_info_list = []
            for stock in self.stocks: 
                stock_info = yf.Ticker(f"{stock.upper()}.NS")
                stock_info_list.append(self.to_stock_quote(stock_info.history(period="1d")))

            return stock_info_list
        except Exception as e:
            logger.error(f"ERROR", "Unable to get stocks information. Reason: {e}")     
            return None

    """
    Mapper function to convert the DataFrame type obj into StockQuote type
    """
    def to_stock_quote(self, symbol: str, df: pd.DataFrame) -> StockQuote:
        latest = df.iloc[-1]

        return StockQuote(
            symbol=symbol,
            date=latest.name.to_pydatetime(),
            open=float(latest["Open"]),
            high=float(latest["High"]),
            low=float(latest["Low"]),
            close=float(latest["Close"]),
            volume=int(latest["Volume"]),
            dividends=float(latest["Dividends"]),
            stock_splits=float(latest["Stock Splits"]),
        )