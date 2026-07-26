# Personal Stocks Tracker

Personal Stocks Tracker is a small Python service that runs as an AWS Lambda function and sends a daily stock briefing to a Telegram chat. It fetches the latest price data for a list of NSE-listed stocks, asks an OpenAI model to summarize the most relevant recent news, and publishes an HTML-formatted update to Telegram.

## What the project does

The application follows this flow:

1. An EventBridge-triggered Lambda function starts the workflow.
2. The code retrieves the latest daily price data for the configured stocks from Yahoo Finance.
3. Each stock is sent to an OpenAI model with a prompt that includes the stock data and instructions for producing a concise briefing.
4. The response is formatted into a Telegram-friendly HTML message and sent to a configured Telegram chat.

## Project structure

- [src/lambda_function.py](src/lambda_function.py) - Lambda entry point.
- [src/interface/StocksInfo.py](src/interface/StocksInfo.py) - Retrieves stock data from Yahoo Finance.
- [src/interface/OpenAIHelper.py](src/interface/OpenAIHelper.py) - Calls the OpenAI Responses API.
- [src/interface/TelegramBotMessenger.py](src/interface/TelegramBotMessenger.py) - Sends the final message to Telegram.
- [src/helper/EnvironmentVars.py](src/helper/EnvironmentVars.py) - Loads environment variables.
- [src/helper/GetSecrets.py](src/helper/GetSecrets.py) - Reads secrets from AWS Secrets Manager.
- [src/helper/SystemPrompt.py](src/helper/SystemPrompt.py) - Defines the system and user prompts for the AI model.
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
- APP_SECRET_NAME: Name of the secret stored in AWS Secrets Manager.
- AI_MODEL: OpenAI model name. Defaults to `gpt-5-mini`.
- BOT_URL: Telegram endpoint URL. Defaults to the standard Telegram sendMessage endpoint.

## Required AWS secret format

The secret referenced by APP_SECRET_NAME should contain at least the following keys:

- api-key: OpenAI API key
- telegram-bot-token: Telegram bot token
- telegram-chat-id: Telegram chat ID

## Deployment notes

This repository is designed to run in an AWS Lambda environment and is intended to be triggered by EventBridge or another scheduled event. The Lambda handler is [src/lambda_function.py](src/lambda_function.py).

## Notes

- The project uses web search capabilities from the OpenAI model to find recent news.
- The final message is generated in HTML so it can be displayed nicely in Telegram.
- The repository currently does not include automated tests.
