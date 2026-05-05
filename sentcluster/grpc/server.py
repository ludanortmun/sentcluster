import grpc
from concurrent import futures
from sentcluster.clusterer import SentenceClusterer
from . import sentence_clusterer_pb2 as pb2
from . import sentence_clusterer_pb2_grpc as pb2_grpc

MIN_BATCH_SIZE = 2
MAX_BATCH_SIZE = 20

class SentenceClustererService(pb2_grpc.SentenceClustererServiceServicer):
    def __init__(self):
        self.clusterer = SentenceClusterer()
        # Warm up the model for fast first request
        self.clusterer.cluster_sentences(["warmup sentence", "another warmup sentence"])

    def ClusterSentences(self, request, context):
        sentences = list(request.sentences)
        if len(sentences) < MIN_BATCH_SIZE:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Too few sentences in the request. Minimum allowed is {MIN_BATCH_SIZE}")
            return pb2.ClusterResponse()
        if len(sentences) > MAX_BATCH_SIZE:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Too many sentences in the request. Maximum allowed is {MAX_BATCH_SIZE}")
            return pb2.ClusterResponse()

        clustered = self.clusterer.cluster_sentences(sentences)
        return pb2.ClusterResponse(sentences=[
            pb2.ClusteredSentence(sentence=s, x=coords[0], y=coords[1], group=label)
            for s, coords, label in clustered
        ])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SentenceClustererServiceServicer_to_server(SentenceClustererService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
