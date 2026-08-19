variable "lambda_s3_key" {
  description = "S3 key (object) for the Lambda deployment package"
  type        = string
  default     = "lambda_code.zip"
}

variable "lambda_function_name" {
  description = "Name for the Lambda function"
  type        = string
  default     = "stocks-tracker-lambda"
}

variable "lambda_handler" {
  description = "Handler for the Lambda function"
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "env" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "lambda_env_vars" {
  description = "Map of environment variables to set on the Lambda (avoid secrets)"
  type        = map(string)
  default = {
    AI_MODEL        = "model"
    APP_SECRET_NAME = "secret"
    BOT_URL         = "url"
    LOG_LEVEL       = "info"
    STOCKS          = "stocks,"
    TIMEZONE        = "Asia/Kolkata"
  }
}

variable "lambda_bucket_name" {
  description = "Bucket name for lambda"
  type        = string
  default     = "my-pers-lambdas"
}

variable "eventbridge_scheduler_name" {
  description = "Eventbridge trigger name"
  type        = string
  default     = "lambda-trigger"
}