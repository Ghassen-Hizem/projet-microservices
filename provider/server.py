import grpc
from concurrent import futures

import money_retrieval_pb2
import money_retrieval_pb2_grpc

class MoneyRetrievalService(money_retrieval_pb2_grpc.MoneyRetrievalServicer):
    def RetrieveMoney(self, request, context):
        amount = request.amount
        return money_retrieval_pb2.MoneyRetrievalResponse(success=True, retrieved_amount=amount)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    money_retrieval_pb2_grpc.add_MoneyRetrievalServicer_to_server(MoneyRetrievalService(), server)
    server.add_insecure_port('[::]:50051') 
    server.start()
    print("Server started, listening on 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
