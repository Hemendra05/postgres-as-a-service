# Postgres as a Service

This project deploys a PostgreSQL service with read-replica architecture on AWS using Terraform, configures the servers with Ansible, and provides API endpoints via FastAPI.

## Components

- **Terraform:** Provisions 3 Ubuntu servers on AWS (1 master, 2 replicas).
- **Ansible:** Configures PostgreSQL and sets up replication.
- **FastAPI:** Offers endpoints to create and destroy resources with user-specified inputs.
- **Docker:** The entire application is containerized.

## Getting Started

### Docker Image

The Docker image is hosted on Docker Hub:
`hemendra05/postgres-as-a-service:v0.0.2`

### Running the Container

Pull and run the container using:
docker pull hemendra05/postgres-as-a-service:v0.0.2

Or Create Docker Image locally using:
`docker build -t postgres-as-a-service:latest .`

And run following command to run application:
`docker run -it -p8080:8080
-e AWS_ACCESS_KEY_ID="AKIAQTS2L"
-e AWS_SECRET_ACCESS_KEY="Hz5rdWxE6jhlcnh67d4nDu"
-e ANSIBLE_HOST_KEY_CHECKING=False
hemendra05/postgres-as-a-service:v0.0.2`


### API Documentation

Once running, access the API docs at:
[http://localhost:8080/documentation](http://localhost:8080/documentation)

## Project Structure Overview

- **terraform/** – Contains Terraform modules for creating AWS infrastructure.
- **ansible/** – Includes playbooks for PostgreSQL setup and dynamic inventory for master/replica configuration.
- **main.py** – FastAPI application that exposes endpoints to deploy and destroy resources.

For a detailed code overview, visit the [GitHub repository](https://github.com/Hemendra05/postgres-as-a-service).
