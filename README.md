# Personal Stocks Tracker

Personal Stocks Tracker is a small Python service that runs as an AWS Lambda function and sends a daily stock briefing to a Telegram chat. It fetches the latest daily price data for a list of NSE-listed stocks, sends that data to an OpenAI model, and publishes an HTML-formatted update to Telegram.

## What the project does

The current implementation follows this flow:

1. An EventBridge-triggered Lambda function starts the workflow.
2. The code reads a comma-separated list of stock symbols from the environment and appends `.NS` to each symbol before fetching data from Yahoo Finance.
3. For each stock, the application sends the latest trading data to OpenAI using the Responses API.
4. On Tuesday and Thursday, the request uses OpenAI web search tooling to try to include a relevant recent news item. On other days, it uses a news-free prompt to keep token usage lower.
5. The generated briefing is combined into a single Telegram message and posted to a configured chat.

## Project structure

- [src/lambda_function.py](src/lambda_function.py) - Lambda entry point and orchestration logic.
- [src/interface/StocksInfo.py](src/interface/StocksInfo.py) - Retrieves stock data from Yahoo Finance.
- [src/interface/OpenAIHelper.py](src/interface/OpenAIHelper.py) - Calls the OpenAI Responses API.
- [src/interface/TelegramBotMessenger.py](src/interface/TelegramBotMessenger.py) - Sends the final message to Telegram.
- [src/helper/EnvironmentVars.py](src/helper/EnvironmentVars.py) - Loads environment variables.
- [src/helper/GetSecrets.py](src/helper/GetSecrets.py) - Reads secrets from AWS Secrets Manager.
- [src/helper/SystemPrompt.py](src/helper/SystemPrompt.py) - Defines the system and user prompts for the AI model.
- [src/models/StockQuote.py](src/models/StockQuote.py) - Data model for the stock quote payload.
- [src/utils/Logger.py](src/utils/Logger.py) - Logging wrapper.

## Requirements

- Python 3.14+
- Dependencies listed in [pyproject.toml](pyproject.toml)

### Main dependencies

- aws-lambda-powertools
- openai
- requests
- yfinance

## Local setup

This project uses uv for dependency management and environment setup.

1. Install uv if it is not already available:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create and sync the environment:

   ```bash
   uv sync
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

4. Set the required environment variables before running the Lambda code locally.

## Environment variables

The application reads the following environment variables from [src/helper/EnvironmentVars.py](src/helper/EnvironmentVars.py):

- STOCKS: Comma-separated stock symbols. The code appends `.NS` for each symbol, so values such as `TCS,RELIANCE` are treated as `TCS.NS` and `RELIANCE.NS`.
- LOG_LEVEL: Logging level. Defaults to `INFO`.
- APP_SECRET_NAME: Name of the secret stored in AWS Secrets Manager. Defaults to `app-secret`.
- AI_MODEL: OpenAI model name. Defaults to `gpt-5-mini`.
- BOT_URL: Telegram endpoint URL. Defaults to `https://api.telegram.org/bot{token}/sendMessage`.

## Required AWS secret format

The secret referenced by APP_SECRET_NAME should contain at least the following keys:

- api-key: OpenAI API key
- telegram-bot-token: Telegram bot token
- telegram-chat-id: Telegram chat ID

The code reads this secret from AWS Secrets Manager using the `ap-south-1` region.

## Deployment notes

This repository is designed to run in an AWS Lambda environment and is intended to be triggered by EventBridge or another scheduled event. The Lambda handler is [src/lambda_function.py](src/lambda_function.py).

## Notes

- The project currently uses OpenAI web search tooling on Tuesday and Thursday only to reduce cost and token usage.
- The final message is generated in HTML so it can be displayed properly in Telegram.
- The repository currently does not include automated tests.
