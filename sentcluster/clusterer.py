from sentence_transformers import SentenceTransformer
from sklearn.cluster import MeanShift
from sklearn.decomposition import PCA


class SentenceClusterer:

    def __init__(self, ):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cluster_model = MeanShift()
        self.dim_reductor = PCA(n_components=2)

    def cluster_sentences(self, sentences: list[str]) -> list[tuple[str, tuple[float, float], int]]:
        embeddings = self._embed_sentences(sentences)
        coords = self._project_embeddings(embeddings)
        labels = self._cluster_embeddings(embeddings)

        return [(s, (c[0], c[1]), l) for s, c, l in zip(sentences, coords, labels)]

    def _project_embeddings(self, embeddings: list[list[float]]) -> list[tuple[float, float]]:
        embeddings_pca = self.dim_reductor.fit_transform(embeddings).tolist()
        return [(x[0], x[1]) for x in embeddings_pca]

    def _embed_sentences(self, sentences: list[str]) -> list[list[float]]:
        return self.embedding_model.encode(sentences).tolist()

    def _cluster_embeddings(self, embeddings: list[list[float]]) -> list[int]:
        self.cluster_model.fit(embeddings)
        return self.cluster_model.labels_.tolist()
