from openai import OpenAI
from helper.GetSecrets import GetSecrets
from utils.Logger import logger
from helper.SystemPrompt import SystemPrompt

class OpenAIHelper:

    def __init__(self, prompt):
        self.client = OpenAI(api_key=GetSecrets.get_secret())
        self.user_prompt = prompt


    def chat_with_ai(self):
        response = self.client.responses.create(
            model="gpt-5-mini",
            input=[
                {
                    "role": "system",
                    "content": SystemPrompt.get_system_prompt()
                },
                {
                    "role": "user",
                    "content": self.user_prompt
                }
            ],
            temperature=0.3
        )

        logger.log("INFO", f"{response.output_text=}")

        return response.output_text

