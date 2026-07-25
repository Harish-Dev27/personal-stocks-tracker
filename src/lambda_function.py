from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.data_classes.event_source  import event_source

from utils.Logger import logger
from helper.EnvironmentVars import stocks
from interface.StocksInfo import StocksInfo
from helper import LambdaResponse
from interface.OpenAIHelper import OpenAIHelper
from helper.SystemPrompt import SystemPrompt


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

    # TODO
    # This feature of calling external news API is cut down as part of costs risks, can be an extensible
    # feature in future

    # Send price information OpenAI model and ask it fetch latest news and give all info mapped with stocks
    stocks_news = []
    for stock in stocks_price:
        ai = OpenAIHelper(SystemPrompt.get_user_prompt(stock))
        stocks_news.append(ai.chat_with_ai())

    logger.log(f"Final content to be served to the user:: {stocks_news}")

    # TODO
    # Send it to end user via telegram bot/AWS SNS

    return LambdaResponse.success_response(200, "Successfully excuted the request")


