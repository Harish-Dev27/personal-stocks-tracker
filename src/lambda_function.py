import json
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.data_classes.event_source  import event_source

from utils.Logger import logger
from helper.EnvironmentVars import stocks
from interface.StocksInfo import StocksInfo

'''
This function will be triggered by Eventbridge scheduler every day once
'''


@event_source(data_class=EventBridgeEvent)
def lambda_handler(event: EventBridgeEvent, context):
    logger.log("INFO", "Lambda invoked")
    logger.log("INFO", f"Received event: {event.raw_event}")

    # Get stocks prices for the current date of time
    st = StocksInfo(stocks)
    stocks_price = st.get_stocks_latest_price()
    logger.log("INFO", f"Stocks info received {stocks_price}")


