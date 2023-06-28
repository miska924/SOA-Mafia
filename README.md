# SOA-Mafia

## Requirements

You need to install Docker & Docker-Compose if have not installed yet.

Follow docker & docker-compose installation guide [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

## Server & 5 bots (autoplay)

```bash
docker compose up --build --scale mafia-client-bot=5
```

## Client

```bash
docker build --no-cache . -t mafia:1.0 && docker run -it --network=mafia-network mafia:1.0 --role client
```

## Generate Protos

```bash
.venv/bin/python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --pyi_out=. -I . app/grpc/schema.proto
```

## Chat client
First of all docker compose needs to be up on chat server. If you want not to play mafia, but just run chat server - you can do this:

```bash
docker compose up redis
```
То run chat you need to use `python3 -m chat` command:

```bash
python3 -m chat --help
```
```
usage: __main__.py [-h] [--chat CHAT] [--host HOST] [--port PORT] [--username USERNAME]

options:
  -h, --help           show this help message and exit
  --chat CHAT
  --host HOST
  --port PORT
  --username USERNAME
```
