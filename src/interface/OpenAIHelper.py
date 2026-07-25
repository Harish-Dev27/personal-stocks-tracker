from openai import OpenAI
from helper.GetSecrets import GetSecrets
from utils.Logger import logger

class OpenAIHelper:

    def __init__(self):
        self.client = OpenAI(api_key=GetSecrets.get_secret())


    def chat_with_ai(self):
        response = self.client.responses.create(
                model="gpt-5-mini",
                input="Write a one-sentence bedtime story about a unicorn."
            )

        logger.log("INFO", f"{response.output_text=}")

        return response.output_text

