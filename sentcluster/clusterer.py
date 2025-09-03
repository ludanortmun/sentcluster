from sentence_transformers import SentenceTransformer
from sklearn.cluster import MeanShift


class SentenceClusterer:

    def __init__(self, ):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cluster_model = MeanShift()

    def cluster_sentences(self, sentences: list[str]) -> dict[int, list[int]]:
        embeddings = self._embed_sentences(sentences)
        labels = self._cluster_embeddings(embeddings)

        clusters = {}
        for label, sentence in zip(labels, sentences):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(sentence)

        return clusters

    def _embed_sentences(self, sentences: list[str]) -> list[list[float]]:
        return self.embedding_model.encode(sentences).tolist()

    def _cluster_embeddings(self, embeddings: list[list[float]]) -> list[int]:
        self.cluster_model.fit(embeddings)
        return self.cluster_model.labels_.tolist()
