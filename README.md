# SOA-Mafia

## Requirements

You need to install Docker & Docker-Compose if have not installed yet.

Follow docker & docker-compose installation guide [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

## Server & 4 bots

```bash
docker compose up --build --scale mafia-client-bot=4
```

## Client

```bash
docker build --no-cache . -t mafia:1.0 && docker run -it --network=mafia-network mafia:1.0 --role client
```

## Generate Protos

```bash
.venv/bin/python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --pyi_out=. -I . app/grpc/schema.proto
```
