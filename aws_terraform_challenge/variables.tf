# Other variables as needed, but no `aws_region` variable here
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_public" {
  description = "CIDR block for the public subnet"
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

