# Docker Setup for Sentcluster

This project has been dockerized with separate containers for the HTTP and gRPC servers.

## Available Docker Images

- **HTTP Server**: Built from `Dockerfile.http` - runs FastAPI server on port 8000
- **gRPC Server**: Built from `Dockerfile.grpc` - runs gRPC server on port 50051

Both images share the same base dependencies and codebase but have different entry points.

## Quick Start

### Using Docker Compose (Recommended)

Build and run both servers:
```bash
docker compose up --build
```

Run specific services:
```bash
# Run only HTTP server
docker compose up http-server

# Run only gRPC server  
docker compose up grpc-server
```

### Using Docker Directly

Build images:
```bash
# Build HTTP server image
docker build -f Dockerfile.http -t sentcluster-http .

# Build gRPC server image
docker build -f Dockerfile.grpc -t sentcluster-grpc .
```

Run containers:
```bash
# Run HTTP server
docker run -p 8000:8000 sentcluster-http

# Run gRPC server
docker run -p 50051:50051 sentcluster-grpc
```

## Important Notes

1. **Model Download**: The sentence transformer model will be downloaded on first startup, which requires internet access and may take a few minutes.

2. **Port Configuration**:
   - HTTP API: http://localhost:8000
   - gRPC service: localhost:50051

3. **Container Size**: The images are approximately 7.7GB due to PyTorch and ML dependencies.

## API Usage

### HTTP API
Once the HTTP container is running, access the API documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

Example request:
```bash
curl -X POST http://localhost:8000/cluster \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["first sentence", "similar first", "completely different", "like the first one"]}'
```

### gRPC API
The gRPC server listens on port 50051. Use any gRPC client with the protocol buffer definition in `sentcluster/grpc/sentence_clusterer.proto`.

## Production Considerations

- Consider using a multi-stage build to reduce image size
- Pre-download models and include them in the image for faster startup
- Use environment variables for configuration
- Add health checks for monitoring
- Consider using a lighter base image like `python:3.11-alpine` if compatible with dependencies