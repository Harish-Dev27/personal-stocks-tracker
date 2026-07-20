import json
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.data_classes.event_source  import event_source

from src.utils.Logger import logger

'''
This function will be triggered by Eventbridge scheduler every day once
'''


@event_source(data_class=EventBridgeEvent)
def lambda_handler(event: EventBridgeEvent, context):
    logger.log("INFO", "Lambda invoked")
    logger.log("INFO", f"Received event: {json.dumps(event)}")


    # TODO
    # Start writing the code to get information about the stocks from reliable API
