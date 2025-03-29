import grpc
import money_retrieval_pb2
import money_retrieval_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = money_retrieval_pb2_grpc.MoneyRetrievalStub(channel)
        response = stub.RetrieveMoney(money_retrieval_pb2.MoneyRetrievalRequest(amount=100.50))
    print("Received response: success={}, retrieved_amount={}".format(response.success, response.retrieved_amount))

if __name__ == '__main__':
    run()