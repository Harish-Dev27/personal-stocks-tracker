from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.data_classes.event_source  import event_source

from utils.Logger import logger
from helper.EnvironmentVars import stocks, app_secret_name
from interface.StocksInfo import StocksInfo
from helper import LambdaResponse
from interface.OpenAIHelper import OpenAIHelper
from interface.TelegramBotMessenger import TelegramBotMessenger
from helper.SystemPrompt import SystemPrompt
from helper.GetSecrets import GetSecrets
from datetime import date


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
    # This feature of calling external news API is cut down as part of costs risks

    app_secret = GetSecrets.get_secret(app_secret_name)

    # Send price information to OpenAI model and ask it to fetch latest news and give all info mapped with stocks
    stocks_news = []
    for stock in stocks_price:
        ai = OpenAIHelper(SystemPrompt.get_user_prompt(stock), app_secret["api-key"])
        stocks_news.append(ai.chat_with_ai())

    final_message = (
            f"<b>📈 Daily Stock Briefing ({date.today():%d %b %Y})</b>\n\n"
            + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(stocks_news)
        )

    logger.log(f"Final content to be served to the user:: {final_message}")

    # Send it to end user via telegram bot
    messenger = TelegramBotMessenger(app_secret)
    messenger.send_message(final_message)

    logger.log("INFO", "Successfully published message to the user")

    return LambdaResponse.success_response(200, "Successfully excuted the request")


