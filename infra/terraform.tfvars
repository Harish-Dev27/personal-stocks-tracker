env                  = "prod"
lambda_s3_key        = "stocks-tracker/lambda.zip"
lambda_function_name = "stocks-tracker"
lambda_bucket_name   = "my-pers-lambdas"
eventbridge_scheduler_name = "stocks-tracker-weekly-trigger"

lambda_env_vars = {
  AI_MODEL        = "gpt-5-mini"
  APP_SECRET_NAME = "app-secret"
  BOT_URL         = "https://api.telegram.org/bot{token}/sendMessage"
  LOG_LEVEL       = "INFO"
  STOCKS          = "GOLDBEES,ITC,TMCV,TMPV,IDFCFIRSTB,KTKBANK"
  TIMEZONE        = "Asia/Kolkata"
}