import grpc
from concurrent import futures
from sentcluster.clusterer import SentenceClusterer
from . import sentence_clusterer_pb2 as pb2
from . import sentence_clusterer_pb2_grpc as pb2_grpc

class SentenceClustererService(pb2_grpc.SentenceClustererServiceServicer):
    def __init__(self):
        self.clusterer = SentenceClusterer()
        # Warm up the model for fast first request
        self.clusterer.cluster_sentences(["warmup sentence", "another warmup sentence"])

    def ClusterSentences(self, request, context):
        clusters = self.clusterer.cluster_sentences(list(request.sentences))
        response = pb2.ClusterResponse()
        for group in clusters.values():
            sg = pb2.SentenceGroup(sentences=group)
            response.sentence_groups.append(sg)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SentenceClustererServiceServicer_to_server(SentenceClustererService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
