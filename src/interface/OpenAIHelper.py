from openai import OpenAI
from helper.GetSecrets import GetSecrets
from utils.Logger import logger
from helper.SystemPrompt import SystemPrompt
from helper.EnvironmentVars import ai_model

class OpenAIHelper:

    def __init__(self, prompt):
        self.client = OpenAI(api_key=GetSecrets.get_secret())
        self.user_prompt = prompt

    """
    Using tool search capabilties instead of external API to cut down cost,
    but its risky that this can cause longer response times causing server compute
    usage being increased as well as extreme use of tokens
    """
    def chat_with_ai(self):
        response = self.client.responses.create(
            model=ai_model,
            tools=[
                {
                    "type": "web_search"
                }
            ],
            input=[
                {
                    "role": "system",
                    "content": SystemPrompt.get_system_prompt()
                },
                {
                    "role": "user",
                    "content": self.user_prompt
                }
            ]
        )

        logger.log("WARN", f"Number of tokens exhausted as part of this request: {response.usage}")

        logger.log("INFO", f"{response.output_text=}")

        return response.output_text

