import io
from flask import Flask, jsonify
from flask import request
import grpc
import json
import money_retrieval_pb2
import money_retrieval_pb2_grpc
from flask import redirect
import requests
from flask_restx import Api, Resource, fields


MAX_LOAN_AMOUNT = 200000

# URL of the Node.js GraphQL endpoint
NODE_APP_URL = "http://localhost:4000/check"

app = Flask(__name__)
api = Api(app, version='1.0',
    title='REST API for making a loan',
    description='Load request REST API service')

ns_customer = api.namespace('Client', description='Client operations')

# the input model of the customer loan
update_customer_model = api.model('CustomerLoan', {
    'id': fields.Integer(required=True, description='The customer ID'),
    'amount': fields.Float(required=True, description='The amount to add to the customer balance')
})

# input model for the form
loan_form_model = api.model('LoanForm', {
    'id': fields.Integer(required=True, description='The customer ID'),
    'nom': fields.String(required=True, description='nom du client'),
    'prenom' : fields.String(required=True, description='prenom du client'),
    'loan_type': fields.String(required=True, description='The loan type, either personal or commercial'),
    'description':fields.String(required=True, description='a brief description about the requested loan'),
    'amount': fields.Float(required=True, description='the loan amount')
})

# the input model of the customer submitted check
submitted_check_model = api.model('CheckModel', {
    'check_number': fields.Integer(required=True, description='The check number'),
    'bank_name': fields.String(required=True, description='The bank name'),
    'bank_address': fields.String(required=True, description='The bank address'),
    'payer_name': fields.String(required=True, description='The payer name'),
    'payee_name': fields.String(required=True, description='The payee name'),
    'amount': fields.Float(required=True, description='The amount'),
    'issue_date': fields.String(required=True, description='The issue date'),
    'memo': fields.String(required=True, description='The memo on the check'),
    'routing_number': fields.Integer(required=True, description='The routing number'),
    'account_number': fields.Integer(required=True, description='The account number')
})


@ns_customer.route("/form" , endpoint='form_ep')
class FormClass(Resource):
    @ns_customer.doc(description='submitting the loan form by including the personal informations and the load amount')
    @ns_customer.expect(loan_form_model, validate=True)
    def post(self):
        if validate_data_received(request.get_json()):
            if (verify_amount(request.get_json()['amount'])):
                return "Form submitted, We'll let you know as soon as the profile is verified !"
            else:
                return "request declined, the amount requested can't be provided !"


@ns_customer.route("/check", endpoint='check_ep')
class CheckClass(Resource):
    def get(self):
        return "Customer profile verified ! please submit a a cashier's check !"
    @ns_customer.doc(description="Submitting a cashier's check")
    @ns_customer.expect(submitted_check_model, validate=True)
    def post(self):
         json_response = verify_check_validity(request.get_json()).data.replace(b"'", b'"')
         my_json = json.load(io.BytesIO(json_response))  
         if(my_json["isValid"]):
            return "the check is verified ! your loan will be transfered to your bank account soon !"


@ns_customer.route("/loan" , endpoint='loan_ep')
class LoanExecutionClass(Resource):
    @ns_customer.doc(description='loan execution by adding a specific amount.')
    @ns_customer.expect(update_customer_model, validate=True)
    def post(self):
        data = request.json
        customer_id = data.get("id")
        amount = data.get("amount")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = money_retrieval_pb2_grpc.MoneyRetrievalStub(channel)
            response = stub.RetrieveMoney(money_retrieval_pb2.MoneyRetrievalRequest(amount))
        print("Received response: success={}, retrieved_amount={}".format(response.success, response.retrieved_amount))
        print("executing loan !")
        a =send_loan_to_bank({
            "id": customer_id,
            "amount": amount
        })
        response = a.data.replace(b"'", b'"')
        my_json = json.load(io.BytesIO(response)) 
        print(my_json)
        return redirect('/success',code=302)



@ns_customer.route("/success" , endpoint='success_ep')
class LoadSuccessCLass(Resource):
    def get(self):
        return "Loan was successful, congrats ! "



########################## UTILITY FUNCTIONS ################################################

def validate_data_received(data: any):
    return data['id'] and data['nom'] and data['prenom']\
          and (data['loan_type'] == "personal" or data['loan_type'] == "commercial") \
          and data['amount'] and data['description']


def verify_amount(amount: any):
    return amount < MAX_LOAN_AMOUNT


def get_financial_profile_activity(data: any):
    return "form submitted ! we'll verify your request and get back to you soon !"


def verify_check_validity(data: any):
    
    graphql_query = {
        "query": """
            query CheckData($data: JSON) {
                check(data: $data)
            }
        """,
        "variables": {
            "data": data
        }
    }

    try:
        response = requests.post(NODE_APP_URL, json=graphql_query)

        response_data = response.json()

        is_valid = response_data.get("data", {}).get("check", False)

        return jsonify({"isValid": is_valid})

    except Exception as e:

        return jsonify({"error": str(e)}), 500
    
def send_loan_to_bank(data: any):

    try:
        customer_id = data["id"]
        amount = data["amount"]

        if not isinstance(customer_id, int) or not isinstance(amount, (int, float)):
            return jsonify({"error": "Invalid input. 'id' must be an integer and 'amount' must be a number."}), 400

        # Define the GraphQL mutation
        graphql_mutation = {
            "query": """
                mutation AddAmountToCustomer($id: Int!, $amount: Float!) {
                    addAmountToCustomer(id: $id, amount: $amount) {
                        id
                        balance
                    }
                }
            """,
            "variables": {
                "id": customer_id,
                "amount": amount
            }
        }

        response = requests.post(NODE_APP_URL, json=graphql_mutation)

        response_data = response.json()

        if "errors" in response_data:
            return jsonify({"error": response_data["errors"]}), 500

        updated_customer = response_data.get("data", {}).get("addAmountToCustomer", {})

        return jsonify({"updatedCustomer": updated_customer})

    except Exception as e:

        return jsonify({"error": str(e)}), 500
    

    ########################## UTILITY FUNCTIONS ################################################

if __name__ == '__main__':
    app.run(debug=True)