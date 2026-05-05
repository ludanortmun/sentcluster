# Sentcluster - Sentence Clustering Tool

Sentcluster clusters sentences by semantic similarity using pretrained sentence embeddings, MeanShift clustering, and a 2D PCA projection for visualization. The project provides both an HTTP API and a gRPC interface, plus a browser UI served by the HTTP app.

## Features

- Sentence embedding using `all-MiniLM-L6-v2` model
- Clustering using MeanShift algorithm
- HTTP API using FastAPI
- Browser UI for interactive clustering and visualization
- gRPC interface

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
├── clusterer.py                    # Core clustering logic
├── http/                           # HTTP API implementation
│   ├── api.py                      # FastAPI routes
│   ├── server.py                   # HTTP server
│   └── static/                     # Browser UI assets
└── grpc/                           # gRPC implementation
    ├── sentence_clusterer.proto    # Protocol buffer definition
    └── server.py                   # gRPC server
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
cd sentcluster/http
PYTHONPATH=../.. python -m sentcluster.http.server
```

The HTTP app will be available at `http://localhost:8000`.

- Browser UI: `GET /`
- Clustering endpoint: `POST /clusters`

#### Browser UI

Open `http://localhost:8000` in your browser to use the built-in UI. You can paste one sentence per line, submit up to 20 sentences, and inspect the resulting 2D scatter plot with color-coded groups and hover tooltips.

#### Request format

`POST /clusters`

```json
{
    "sentences": [
        "The cat is on the roof.",
        "A dog is in the garden.",
        "The sun is shining brightly."
    ]
}
```

#### Response format

```json
{
  "sentences": [
    {
      "sentence": "The cat is on the roof.",
      "x": -0.6680696763722918,
      "y": 0.37411267249589797,
      "group": 0
    },
    {
      "sentence": "A dog is in the garden.",
      "x": -0.004630542536244918,
      "y": -0.740552529543497,
      "group": 0
    },
    {
      "sentence": "The sun is shining brightly.",
      "x": 0.6727002189085364,
      "y": 0.36643985704759896,
      "group": 1
    }
  ]
}
```

Each returned item includes:

- `sentence`: the original input sentence
- `x` and `y`: the PCA-projected 2D coordinates
- `group`: the cluster label assigned by MeanShift

#### Constraints and behavior

- The request accepts between `2` and `20` sentences per batch.
- Blank-line filtering is handled by the browser UI before submission.
- The HTTP API returns projected 2D coordinates so the results can be plotted directly.

Example request:
```bash
curl -X POST http://localhost:8000/clusters \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["first sentence", "similar first", "completely different", "like the first one"]}'
```

### gRPC

Start the gRPC server:
```bash
python -m sentcluster.grpc.server
```

The gRPC server will listen on port 50051 by default.

The gRPC `ClusterSentences` method enforces the same input bounds as HTTP: between `2` and `20` sentences per request.

## Dependencies

- scikit-learn
- sentence-transformers
- FastAPI
- uvicorn
- gRPC
- gRPC-tools
