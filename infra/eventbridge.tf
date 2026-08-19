resource "aws_iam_role" "scheduler_invoke_role" {
  name = "stocks-tracker-scheduler-invoke"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "scheduler.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "scheduler_invoke_policy" {
  name = "stocks-tracker-scheduler-invoke-policy"
  role = aws_iam_role.scheduler_invoke_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["lambda:InvokeFunction"]
        Resource = [aws_lambda_function.stocks_tracker.arn]
      }
    ]
  })
}

resource "aws_scheduler_schedule" "weekly_tuesday" {
  name                         = var.eventbridge_scheduler_name
  description                  = "Triggers stocks-tracker Lambda every Tuesday"
  schedule_expression          = "cron(30 9 ? * TUE *)"
  schedule_expression_timezone = "Asia/Calcutta"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.stocks_tracker.arn
    role_arn = aws_iam_role.scheduler_invoke_role.arn
    input    = jsonencode({})
  }
}
