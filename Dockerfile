FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt
ENV PATH="/root/.local/bin:$PATH"
COPY . .

FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    unzip \
    software-properties-common \
    gnupg \
    ansible \
    git \
    wget && \
    \
    wget https://releases.hashicorp.com/terraform/1.10.5/terraform_1.10.5_linux_amd64.zip && \
    unzip terraform_1.10.5_linux_amd64.zip -d /usr/local/bin/ && \
    rm -rf terraform_1.10.5_linux_amd64.zip && \
    apt-get purge -y git wget software-properties-common gnupg && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
ENV PATH="/root/.local/bin:$PATH"

EXPOSE 8080

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
