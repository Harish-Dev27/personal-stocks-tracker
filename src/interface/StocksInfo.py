import yfinance as yf
from utils.Logger import logger

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
                stock_info_list.append({stock : stock_info.history(period="1d")})

            return stock_info_list
        except Exception as e:
            logger.error(f"ERROR", "Unable to get stocks information. Reason: {e}")     
            return None