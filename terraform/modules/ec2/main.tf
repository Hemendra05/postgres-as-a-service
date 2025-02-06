resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "${var.project}-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-public-subnet-${count.index + 1}"
  }
}


resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(var.public_subnets)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-private-rt"
  }
}


resource "aws_security_group" "postgres" {
  name        = "${var.project}-sg"
  description = "Security group for PostgreSQL as a Service"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "PostgreSQL as a Service"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = var.allowed_cidr_blocks
  }

  tags = {
    Name = "${var.project}-sg"
  }
}

# Generate a new RSA key pair.
resource "tls_private_key" "ec2_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create an AWS key pair using the generated public key.
resource "aws_key_pair" "ec2_key" {
  key_name   = "${var.project}-key"
  public_key = tls_private_key.ec2_key.public_key_openssh
}

# Optionally, write the private key to a file (make sure the destination directory exists).
resource "local_file" "ec2_key_private" {
  content         = tls_private_key.ec2_key.private_key_pem
  filename        = "${path.module}/../../keys/${var.project}-key.pem"
  file_permission = "0600"
}


resource "aws_instance" "postgres_primary" {
  count                       = var.postgres_primary_replica_count
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.ec2_key.key_name
  subnet_id                   = aws_subnet.public[count.index].id
  availability_zone           = var.availability_zones[0]
  vpc_security_group_ids      = [aws_security_group.postgres.id]
  associate_public_ip_address = true
  tags = {
    Name = "${var.project}-primary"
  }
}

resource "aws_instance" "postgres_replica" {
  count                       = var.postgres_replica_replica_count
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.ec2_key.key_name
  subnet_id                   = aws_subnet.public[0].id
  availability_zone           = var.availability_zones[0]
  vpc_security_group_ids      = [aws_security_group.postgres.id]
  associate_public_ip_address = true
  tags = {
    Name = "${var.project}-replica-${count.index + 1}"
  }
}
