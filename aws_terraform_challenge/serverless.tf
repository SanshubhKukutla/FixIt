# Lambda Function
resource "aws_lambda_function" "example_lambda" {
  filename         = "lambda_function.zip"
  function_name    = "example_lambda"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec_role.arn
}

# API Gateway for Lambda
resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "example_api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.api_gateway.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.example_lambda.invoke_arn
}
