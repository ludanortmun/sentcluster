from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from sentcluster.clusterer import SentenceClusterer


@asynccontextmanager
async def lifespan(_app):
    clusterer = SentenceClusterer()
    # Warm up the model
    clusterer.cluster_sentences(["warmup sentence", "another warmup sentence"])
    _app.state.clusterer = clusterer
    yield  # No shutdown logic needed


app = FastAPI(lifespan=lifespan)


class ClusterRequest(BaseModel):
    sentences: List[str]


class ClusterResponse(BaseModel):
    sentence_groups: List[List[str]]


@app.post("/cluster", response_model=ClusterResponse)
def cluster_sentences(request: ClusterRequest):
    clusterer = app.state.clusterer
    clusters = clusterer.cluster_sentences(request.sentences)
    grouped = list(clusters.values())
    return ClusterResponse(sentence_groups=grouped)
