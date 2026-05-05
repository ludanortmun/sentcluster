from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, model_validator

from sentcluster.clusterer import SentenceClusterer

MIN_BATCH_SIZE = 2
MAX_BATCH_SIZE = 20

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

    @model_validator(mode='after')
    def check_array_max_length(self):
        if len(self.sentences) < MIN_BATCH_SIZE:
            raise ValueError('Too few sentences in the request. Minimum allowed is {}'.format(MIN_BATCH_SIZE))
        if len(self.sentences) > MAX_BATCH_SIZE:
            raise ValueError('Too many sentences in the request. Maximum allowed is {}'.format(MAX_BATCH_SIZE))
        return self

class ClusteredSentence(BaseModel):
    sentence: str
    x: float
    y: float
    group: int

class ClustersResponse(BaseModel):
    sentences: List[ClusteredSentence]


@app.post("/clusters", response_model=ClustersResponse)
def cluster_sentences(request: ClusterRequest):
    clusterer = app.state.clusterer
    clustered = clusterer.cluster_sentences(request.sentences)
    return ClustersResponse(sentences=[
        ClusteredSentence(sentence=s, x=coords[0], y=coords[1], group=label) for s, coords, label in clustered
    ])


app.mount("/", StaticFiles(directory="static", html=True), name="static")