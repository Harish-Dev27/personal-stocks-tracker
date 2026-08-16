resource "aws_lambda_function" "stocks_tracker" {
  function_name = var.lambda_function_name
  s3_bucket     = aws_s3_bucket.lambda_code.bucket
  s3_key        = var.lambda_s3_key
  handler       = var.lambda_handler
  runtime       = "python3.14"
  role          = aws_iam_role.lambda_exec.arn
  publish       = false
  timeout       = 300
  memory_size   = 512
  description   = "Lambda to get info about preferred stocks"

  environment {
    variables = var.lambda_env_vars
  }

  lifecycle {
    ignore_changes = ["layers"]
  }

  tags = {
    Name = var.lambda_function_name
    Env  = var.env
  }
}

output "lambda_function_name" {
  value = aws_lambda_function.stocks_tracker.function_name
}

