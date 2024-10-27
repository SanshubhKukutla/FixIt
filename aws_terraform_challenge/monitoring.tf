# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/example_lambda"
  retention_in_days = 7
}

# SNS Topic for Notifications
resource "aws_sns_topic" "example_sns" {
  name = "example_topic"
}

# SNS Subscription
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.example_sns.arn
  protocol  = "email"
  endpoint  = "example@example.com"  # Replace with your email
}
