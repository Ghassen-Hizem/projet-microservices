from flask import Flask
from flask import request
import json
import grpc
import money_retrieval_pb2
import money_retrieval_pb2_grpc

MAX_LOAN_AMOUNT = 200000

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Welcome to the Loan request service, would you like to request a loan ?"


@app.route("/get-form")
def getForm():
    return "Kindly submit this form in order to make a Load request, please provide your ID, your personal information, the loan type that you like to make\
        specify the loan amount and a brief description."

@app.post('/post-form')
def postForm():
    if validate_data_received(request.get_json()):
        if (verify_amount(request.get_json()['amount'])):
            return get_financial_profile_activity(request.get_json())
        else:
            return "request declined, the amount requested can't be provided !"
        
@app.route("/test")
def testing_grpc():
    with grpc.insecure_channel('localhost:50051') as channel:
         stub = money_retrieval_pb2_grpc.MoneyRetrievalStub(channel)
         response = stub.RetrieveMoney(money_retrieval_pb2.MoneyRetrievalRequest(amount=100.50))
    return "Received response: success={}, retrieved_amount={}".format(response.success, response.retrieved_amount)


def validate_data_received(data: any):
    return data['id'] and data['nom'] and data['prenom']\
          and (data['loan_type'] == "personal" or data['loan_type'] == "commercial") \
          and data['amount'] and data['description']

def verify_amount(amount: any):
    return amount < MAX_LOAN_AMOUNT

def get_financial_profile_activity(data: any):
    return "form submitted ! we'll verify your request and get back to you soon !"