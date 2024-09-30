# FIAP - Health Med Auth Service

**Auth adapters**

- AWS Cognito

## Requirements

- Docker
- Docker Compose

## Usage

### Local

1.Make sure to correctly configure your docker-compose.yaml

```yaml
app:
  build:
    context: .
    dockerfile: Dockerfile
  ports:
    - "8001:80"
  volumes:
    - .:/app/:rw
    - ~/.aws:/root/.aws
  networks:
    - app-network
  environment:
    # Development
    # ===================================================== #
    # - AWS_REGION_NAME=us-east-1
    # - ENVIRONMENT=development
    # Local
    # ===================================================== #
    - ENVIRONMENT=local
    - AWS_ENDPOINT_URL=http://motoserver:4566
    - AWS_ACCESS_KEY_ID=test
    - AWS_SECRET_ACCESS_KEY=test
  command: uvicorn main:app --host 0.0.0.0 --port 80 --reload
  depends_on:
    - motoserver
```

- **Run**:

```sh
make run ENV=local
```

- **Destroy**:

```sh
docker compose down -v
```

you may access the application at http://localhost:8001/auth/docs.

### Development

1. Set your aws credentials at `~/.aws/credentials`
2. Make sure to correctly configure your docker-compose.yaml

```yaml
app:
  build:
    context: .
    dockerfile: Dockerfile
  ports:
    - "8001:80"
  volumes:
    - .:/app/:rw
    - ~/.aws:/root/.aws
  networks:
    - app-network
  environment:
    # Development
    # ===================================================== #
    - AWS_REGION_NAME=us-east-1
    - ENVIRONMENT=development
    # Local
    # ===================================================== #
    # - ENVIRONMENT=local
    # - AWS_ENDPOINT_URL=http://motoserver:4566
    # - AWS_ACCESS_KEY_ID=test
    # - AWS_SECRET_ACCESS_KEY=test
  command: uvicorn main:app --host 0.0.0.0 --port 80 --reload
  depends_on:
    - motoserver
```

- **Run**:

```sh
make terraform-init ENV=dev && \
make terraform-apply ENV=dev && \
make app
```

- **Destroy**:

```sh
docker compose down -v
```

you may access the application at http://localhost:8001/auth/docs.
