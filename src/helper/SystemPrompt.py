from dataclasses import asdict
import json

class SystemPrompt:

    def __init__(self):
        pass

    @staticmethod
    def get_system_prompt():
        return """
            You are a financial news assistant.

            You will receive today's trading data for one NSE-listed stock.

            Using web search, identify the single most relevant recent news item for that company.

            Return:

            # <Company>

            Close:
            Today's Change:

            News:
            <Maximum 2 sentences>

            Source:
            <URL>

            Takeaway:
            <Maximum 2 sentences>

            Rules:
            - Search only for this company.
            - Use only one news item.
            - Keep the total response under 100 words.
            - Do not provide investment advice.  
        """

    @staticmethod
    def get_user_prompt(stocks_info):
        payload = {
            "stocks": [
                {
                    **asdict(stock),
                    "date": stock.date.isoformat()
                }
                for stock in stocks_info
            ]
        }

        return f"""
            Generate today's stock briefing.

            Requirements:
            - Cover every stock.
            - Keep each stock section under 150 words.
            - The complete response should be readable in about 5 minutes for 5–8 stocks.
            - Prioritize clarity over technical analysis.

            Stock data:
            {json.dumps(payload, indent=2)}
        """