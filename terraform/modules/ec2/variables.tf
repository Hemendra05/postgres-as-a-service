variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default = "t3a.small"
}

variable "availability_zones" {
  description = "Availability zones for EC2 instances"
  type        = list(string)
}

variable "postgres_primary_replica_count" {
  description = "Number of replicas for primary server"
  type        = number
  default = 1
}

variable "postgres_replica_replica_count" {
  description = "Number of replicas for replica server"
  type        = number
  default = 2
}




variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnets" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
}

variable "project" {
  description = "Project name"
  type        = string
}

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access PostgreSQL"
  type        = list(string)
}
