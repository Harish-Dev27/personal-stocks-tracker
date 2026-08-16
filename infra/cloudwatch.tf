resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.stocks_tracker.function_name}"
  retention_in_days = 14

  tags = {
    Name = "lambda-log-${aws_lambda_function.stocks_tracker.function_name}"
    Env  = var.env
  }

  depends_on = [aws_lambda_function.stocks_tracker]
}
