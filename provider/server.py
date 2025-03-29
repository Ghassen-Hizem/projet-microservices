import grpc
from concurrent import futures

# Assuming you have a proto file named 'money_retrieval.proto'
# and generated Python code from it using protoc:
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. money_retrieval.proto
import money_retrieval_pb2
import money_retrieval_pb2_grpc

class MoneyRetrievalService(money_retrieval_pb2_grpc.MoneyRetrievalServicer):
    def RetrieveMoney(self, request, context):
        amount = request.amount
        return money_retrieval_pb2.MoneyRetrievalResponse(success=True, retrieved_amount=amount)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    money_retrieval_pb2_grpc.add_MoneyRetrievalServicer_to_server(MoneyRetrievalService(), server)
    server.add_insecure_port('[::]:50051') # Make sure this port is available
    server.start()
    print("Server started, listening on 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

# money_retrieval.proto example:

# syntax = "proto3";

# service MoneyRetrieval {
#   rpc RetrieveMoney (MoneyRetrievalRequest) returns (MoneyRetrievalResponse) {}
# }

# message MoneyRetrievalRequest {
#   double amount = 1;
# }

# message MoneyRetrievalResponse {
#   bool success = 1;
#   double retrieved_amount = 2;
# }