# S3 Bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "terraform-example-bucket"
}

# EFS (Elastic File System)
resource "aws_efs_file_system" "efs" {
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }
}
