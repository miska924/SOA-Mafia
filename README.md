# SOA-Mafia

### Proto
```
.venv/bin/python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --pyi_out=. -I . src/grpc/schema.proto
```