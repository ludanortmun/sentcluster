# Sentcluster - Sentence Clustering Tool

Simple sentence clustering tool using pre-trained sentence embeddings and clustering algorithms. This service provides both HTTP and gRPC interfaces for clustering sentences into semantically similar groups.

## Features

- Sentence embedding using `all-MiniLM-L6-v2` model
- Clustering using MeanShift algorithm
- HTTP API using FastAPI
- gRPC interface
- Python SDK

## Installation

### Local Installation
```bash
pip install -r requirements.txt
```

### Docker Installation
The project includes Docker support for both HTTP and gRPC servers:

```bash
# Build and run both servers with docker-compose
docker compose up --build

# Or run individually:
docker build -f Dockerfile.http -t sentcluster-http .
docker run -p 8000:8000 sentcluster-http
```

See [DOCKER.md](DOCKER.md) for detailed Docker usage instructions.

## Project Structure

```
sentcluster/
├── clusterer.py       # Core clustering logic
├── http/              # HTTP API implementation
│   ├── api.py         # FastAPI routes
│   └── server.py      # HTTP server
└── grpc/              # gRPC implementation
    ├── sentence_clusterer.proto  # Protocol buffer definition
    └── server.py      # gRPC server
```

## Generate gRPC Code

Before running the gRPC server, generate the Python gRPC code:

```bash
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. sentcluster/grpc/sentence_clusterer.proto
```

## Usage

### HTTP API

Start the HTTP server:
```bash
python -m sentcluster.http.server
```

The API will be available at http://localhost:8000

Example request:
```bash
curl -X POST http://localhost:8000/cluster \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["first sentence", "similar first", "completely different", "like the first one"]}'
```

### gRPC

Start the gRPC server:
```bash
python -m sentcluster.grpc.server
```

The gRPC server will listen on port 50051 by default.

## Dependencies

- scikit-learn
- sentence-transformers
- FastAPI
- uvicorn
- gRPC
- gRPC-tools
