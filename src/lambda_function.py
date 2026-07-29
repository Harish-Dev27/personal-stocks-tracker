from datetime import date, datetime
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.data_classes.event_source import event_source

from helper import LambdaResponse
from helper.EnvironmentVars import app_secret_name, ist, stocks
from helper.GetSecrets import GetSecrets
from helper.SystemPrompt import SystemPrompt
from interface.OpenAIHelper import OpenAIHelper
from interface.StocksInfo import StocksInfo
from interface.TelegramBotMessenger import TelegramBotMessenger
from utils.Logger import logger




@event_source(data_class=EventBridgeEvent)
@logger._logger(clear_state=True)
def lambda_handler(event: EventBridgeEvent, context):
    """
    This function will be triggered by Eventbridge scheduler once every week on Mon-Fri only
    Cron expression has been adjusted accordingly
    """

    try:
        logger.log("INFO", "Lambda invoked")
        logger.log("INFO", f"Received event: {event.raw_event}")

        # Get stocks prices for the current date and time
        st = StocksInfo(stocks)
        stocks_price = st.get_stocks_latest_price()
        logger.log("INFO", f"Stocks info received {stocks_price}")

        app_secret = GetSecrets.get_secret(app_secret_name)

        # Send price information to OpenAI model
        stocks_news = []
        for stock in stocks_price:
            ai = OpenAIHelper(SystemPrompt.get_user_prompt(stock), app_secret["api-key"], True if should_fetch_news() else False)
            stocks_news.append(ai.chat_with_ai())


        final_message = (
                f"<b>📈 Daily Stock Briefing ({date.today():%d %b %Y})</b>\n\n"
                + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(stocks_news)
            )

        logger.log("INFO", f"Final content to be served to the user:: {final_message}")

        # Send it to end user via telegram bot
        messenger = TelegramBotMessenger(app_secret)
        messenger.send_message(final_message)

        logger.log("INFO", "Successfully published message to the user")

        return LambdaResponse.success_response(200, "Successfully executed the request")
    except Exception as e:
        logger.log("ERROR", f"Unable to complete the request successfully. Reason {e}")
        return LambdaResponse.error_response(500, "Server error")




def should_fetch_news() -> bool:
    """
    Returns True only on Tuesday and Thursday (IST).
    This is actually an extra check to avoid unnecessary token exhaustion, as Cloudwatch 
    triggers on Monday and Tuesday only
    """
    today = datetime.now(ist).weekday()

    # Monday=0, Tuesday=1, Wednesday=2,
    # Thursday=3, Friday=4, Saturday=5, Sunday=6
    logger.log("INFO", f"Today is {datetime.now(IST)}, hence invoking AI for news accordingly.")
    return today in (1, 3)


