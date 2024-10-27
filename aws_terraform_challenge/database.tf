# RDS Instance
resource "aws_db_instance" "db_instance" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "exampledb"
  username             = "admin"
  password             = "password123"
}

# DynamoDB Table
resource "aws_dynamodb_table" "dynamodb_table" {
  name         = "ExampleTable"
  hash_key     = "ID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "ID"
    type = "S"
  }
}
