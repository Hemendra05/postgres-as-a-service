provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket         = "codepipeline-qwerty"
    key            = "postgres-as-a-service/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}


module "ec2" {
  source = "./modules/ec2"
  ami_id = var.ami_id
  project = var.project
  availability_zones = var.availability_zones
  vpc_cidr = var.vpc_cidr
  public_subnets = var.public_subnets
  allowed_cidr_blocks = var.allowed_cidr_blocks
}
