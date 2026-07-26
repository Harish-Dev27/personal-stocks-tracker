from openai import OpenAI
from utils.Logger import logger
from helper.SystemPrompt import SystemPrompt
from helper.EnvironmentVars import ai_model

class OpenAIHelper:

    def __init__(self, prompt, key, should_fetch_news = False):
        self.client = OpenAI(api_key=key)
        self.user_prompt = prompt
        self.fetch_news = should_fetch_news

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
            text={
                "verbosity": "low"
            },
            input=[
                {
                    "role": "system",
                    "content": (
                        SystemPrompt.get_system_prompt()
                        if self.fetch_news
                        else SystemPrompt.get_news_free_sys_prompt()
                    )
                },
                {
                    "role": "user",
                    "content": self.user_prompt
                }
            ]
        )

        usage = response.usage

        logger.log("WARN",
            f"Stock {self.user_prompt} - input={usage.input_tokens} output={usage.output_tokens} total={usage.total_tokens}",
        )

        logger.log("INFO", f"{response.output_text=}")

        return response.output_text

