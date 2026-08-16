resource "aws_s3_bucket" "lambda_code" {
  bucket        = var.lambda_bucket_name
  force_destroy = false

  tags = {
    Name = "lambda-code"
    Env  = var.env
  }
}

resource "aws_s3_bucket_versioning" "lambda_bucket_versioning" {
  bucket = aws_s3_bucket.lambda_code.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lambda_bucket_sse" {
  bucket = aws_s3_bucket.lambda_code.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "lambda_block_public" {
  bucket = aws_s3_bucket.lambda_code.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "lambda_code_bucket" {
  value = aws_s3_bucket.lambda_code.bucket
}