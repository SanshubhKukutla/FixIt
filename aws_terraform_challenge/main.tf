# Specify the required Terraform version
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Outputs (ensure these are not duplicated in outputs.tf)
output "s3_bucket_name" {
  value = aws_s3_bucket.my_bucket.bucket
}

output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

output "lambda_function_arn" {
  value = aws_lambda_function.example_lambda.arn
}
