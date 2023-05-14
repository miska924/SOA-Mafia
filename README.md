# SOA-Mafia

## Requirements

You need to install Docker & Docker-Compose if have not installed yet.

Follow docker & docker-compose installation guide [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

## Server

```bash
docker compose up
```

## Client

```bash
docker build -t mafia:1.0 && docker run mafia:1.0 --role client
```

## Generate Protos

```bash
.venv/bin/python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --pyi_out=. -I . app/grpc/schema.proto
```
