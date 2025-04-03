import io
from flask import Flask, Response, jsonify
from flask import request
import grpc
import json
from zeep import Client
from zeep.transports import Transport
import money_retrieval_pb2
import re
import xml.etree.ElementTree as ET
import money_retrieval_pb2_grpc
import requests
import os
from requests import Session
from zeep.exceptions import Fault
from flask_restx import Api, Resource, fields


MAX_LOAN_AMOUNT = 200000

os.environ["Mainresponse"] = "Loan not submitted yet, please submit a request !"

os.environ["customer_id"]  = "C1003"


NODE_APP_URL = "http://localhost:4000/check"

SOAP_ENDPOINT = "http://localhost:8080/axis2/services/CustomerFinancialProfileService.CustomerFinancialProfileServiceHttpSoap11Endpoint/"  # Replace with your actual SOAP endpoint
SOAP_WSDL = None  

app = Flask(__name__)
api = Api(app, version='1.0',
    title='REST API for making a loan',
    description='Load request REST API service')

ns_customer = api.namespace('Client', description='Client operations')

# the input model of the customer loan
update_customer_model = api.model('CustomerLoan', {
    'id': fields.String(required=True, description='The customer ID'),
    'amount': fields.Float(required=True, description='The amount to add to the customer balance')
})

# input model for the form
loan_form_model = api.model('LoanForm', {
    'id': fields.String(required=True, description='The customer ID'),
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
        os.environ["amount"] = request.get_json()['amount']
        print("wiiiiw : ", os.environ.get("amount"))
        if validate_data_received(request.get_json()):
            if (verify_amount(request.get_json()['amount'])):
                os.environ["customer_id"] = request.get_json()["id"]
                os.environ["Mainresponse"] = "Form submitted, We'll let you know as soon as the profile is verified !"
                return "Form submitted, We'll let you know as soon as the profile is verified !"
            else:
                os.environ["Mainresponse"] = "request declined, the amount requested can't be provided !"
                return "request declined, the amount requested can't be provided !"


@ns_customer.route("/check", endpoint='check_ep')
class CheckClass(Resource):
    @ns_customer.doc(description="Submitting a cashier's check")
    @ns_customer.expect(submitted_check_model, validate=True)
    def post(self):
         risk_response = calculate_risk(get_risk_profile(get_financial_profile_activity(os.environ["customer_id"]).get_data())).get_data()
         risk_assesement = risk_response.replace(b"'", b'"')
         risk_assesement = json.load(io.BytesIO(risk_assesement))    
         if(risk_assesement["riskAssessment"]["riskCategory"]=="Medium Risk" or risk_assesement["riskAssessment"]["riskCategory"] =="Low Risk"):
            json_response = verify_check_validity(request.get_json()).data.replace(b"'", b'"')
            my_json = json.load(io.BytesIO(json_response))  
            if(my_json["isValid"]):
                os.environ["Mainresponse"] = "the check is verified ! your loan will be transfered to your bank account soon !"
                return "the check is verified ! your loan will be transfered to your bank account soon !"


@ns_customer.route("/loan" , endpoint='loan_ep')
class LoanExecutionClass(Resource):
    @ns_customer.doc(description='loan execution by adding a specific amount.')
    @ns_customer.expect(update_customer_model, validate=True)
    def post(self):
        data = request.json
        customer_id = data.get("id")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = money_retrieval_pb2_grpc.MoneyRetrievalStub(channel)
            response = stub.RetrieveMoney(money_retrieval_pb2.MoneyRetrievalRequest(amount=os.environ.get("amount")))
        print("Received response: success={}, retrieved_amount={}".format(response.success, response.retrieved_amount))
        print("executing loan !")
        a =send_loan_to_bank({
            "id": customer_id,
            "amount": os.environ.get("amount")
        })
        response = a.data.replace(b"'", b'"')
        my_json = json.load(io.BytesIO(response)) 
        print(my_json)
        os.environ["Mainresponse"] = "Your loan is transferred to your bank account, thanks for your trust"
        return "Your loan is transferred to your bank account, thanks for your trust"


@ns_customer.route("/loan-status" , endpoint='success_ep')
class LoadSuccessCLass(Resource):
    def get(self):     
        return os.environ.get("Mainresponse")   


########################## UTILITY FUNCTIONS ################################################

def validate_data_received(data: any):
    return data['id'] and data['nom'] and data['prenom']\
          and (data['loan_type'] == "personal" or data['loan_type'] == "commercial") \
          and data['amount'] and data['description']


def verify_amount(amount: any):
    return amount < MAX_LOAN_AMOUNT


def get_financial_profile_activity(customer_id: any):
    try:
        # Créer une session
        session = Session()
        transport = Transport(session=session)
        
        # Vérifier si WSDL est configuré
        if SOAP_WSDL:
            # Méthode 1: Utilisation de WSDL avec zeep
            client = Client(SOAP_WSDL, transport=transport)
            result = client.service.getCustomerFinancialProfile(customerId=customer_id)
            # Convertir le résultat en chaîne
            return Response(str(result), mimetype='text/plain')
        else:
            # Méthode 2: Requête SOAP directe sans WSDL
            envelope = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.finrisk.root">
               <soapenv:Header/>
               <soapenv:Body>
                  <ser:getCustomerFinancialProfile>
                     <ser:customerId>{customer_id}</ser:customerId>
                  </ser:getCustomerFinancialProfile>
               </soapenv:Body>
            </soapenv:Envelope>
            """
            
            headers = {
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': 'urn:getCustomerFinancialProfile'
            }
            
            response = session.post(SOAP_ENDPOINT, data=envelope, headers=headers)
            
            # Vérifier si la requête a réussi
            if response.status_code == 200:
                return Response(response.text, mimetype='text/xml')
            else:
                return f"Échec de l'appel SOAP avec le code d'état {response.status_code}", 500
    
    except Fault as soap_fault:
        return f"Erreur SOAP: {str(soap_fault)}", 400
    except Exception as e:
        return f"Erreur: {str(e)}", 500



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
    
def get_risk_profile(response: any):

    if isinstance(response, bytes):
        soap_response = response.decode('utf-8')
    
    
     # Parse XML
    # First, remove the XML declaration if present
    soap_response = re.sub(r'<\?xml.*?\?>', '', soap_response, flags=re.DOTALL)
    
    # Define namespaces for proper parsing
    namespaces = {
        'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ns': 'http://service.finrisk.root',
        'ax21': 'http://service.finrisk.root/xsd',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    
    # Parse the XML string
    root = ET.fromstring(soap_response)
    
    # Navigate to the CustomerFinancialProfile element
    profile_element = root.find('.//ns:return[@xsi:type="ax21:CustomerFinancialProfile"]', namespaces)
    if profile_element is None:
        return json.dumps({"error": "CustomerFinancialProfile not found in response"})
    
    # Extract basic customer data
    customer_data = {
        "accountAge": get_element_text(profile_element, './ax21:accountAge', namespaces),
        "creditScore": get_element_text(profile_element, './ax21:creditScore', namespaces),
        "customerId": get_element_text(profile_element, './ax21:customerId', namespaces),
        "customerName": get_element_text(profile_element, './ax21:customerName', namespaces),
        "suspiciousActivities": [],
        "transactions": []
    }
    
    # Convert types
    if customer_data["accountAge"]:
        customer_data["accountAge"] = int(customer_data["accountAge"])
    if customer_data["creditScore"]:
        customer_data["creditScore"] = int(customer_data["creditScore"])
    
    # Extract suspicious activities
    suspicious_elements = profile_element.findall('./ax21:suspiciousActivities[@xsi:type="ax21:SuspiciousActivity"]', namespaces)
    for elem in suspicious_elements:
        activity = {
            "activityId": get_element_text(elem, './ax21:activityId', namespaces),
            "activityType": get_element_text(elem, './ax21:activityType', namespaces),
            "description": get_element_text(elem, './ax21:description', namespaces),
            "severity": get_element_text(elem, './ax21:severity', namespaces),
            "timestamp": get_element_text(elem, './ax21:timestamp', namespaces),
            "verified": get_element_text(elem, './ax21:verified', namespaces)
        }
        
        # Convert types
        if activity["severity"]:
            activity["severity"] = int(activity["severity"])
        if activity["verified"]:
            activity["verified"] = activity["verified"].lower() == "true"
            
        customer_data["suspiciousActivities"].append(activity)
    
    # Extract transactions
    transaction_elements = profile_element.findall('./ax21:transactions[@xsi:type="ax21:Transaction"]', namespaces)
    for elem in transaction_elements:
        transaction = {
            "amount": get_element_text(elem, './ax21:amount', namespaces),
            "country": get_element_text(elem, './ax21:country', namespaces),
            "timestamp": get_element_text(elem, './ax21:timestamp', namespaces),
            "transactionId": get_element_text(elem, './ax21:transactionId', namespaces),
            "type": get_element_text(elem, './ax21:type', namespaces)
        }
        
        # Convert types
        if transaction["amount"]:
            transaction["amount"] = float(transaction["amount"])
            
        customer_data["transactions"].append(transaction)
    
    # Return formatted JSON
    return customer_data

def get_element_text(element, xpath, namespaces):
    """Helper function to extract text from an element"""
    elem = element.find(xpath, namespaces)
    if elem is not None and elem.text:
        return elem.text
    return None

def calculate_risk(response : any):
    try:
        profile_data = {
            'customerId': response['customerId'],
            'customerName': response['customerName'],
            'accountAge': response['accountAge'],
            'creditScore': response['creditScore'],
            'transactions': [],
            'suspiciousActivities': []
        }
        
        # Process transactions if present
        if hasattr(response, 'transactions') and response.transactions:
            profile_data['transactions'] = [
                {
                    'transactionId': tx['transactionId'],
                    'amount': tx['amount'],
                    'type': tx['type'],
                    'timestamp': tx['timestamp'],
                    'country': tx['country']
                }
                for tx in response.transactions
            ]
        
        # Process suspicious activities if present
        if hasattr(response, 'suspiciousActivities') and response.suspiciousActivities:
            profile_data['suspiciousActivities'] = [
                {
                    'activityId': act['activityId'],
                    'activityType': act['activityType'],
                    'severity': act['severity'],
                    'description': act['description'],
                    'timestamp': act['timestamp']
                }
                for act in response.suspiciousActivities
            ]
        
        # Calculate risk score and category
        risk_score = calculate_risk_score(profile_data)
        risk_category = get_risk_category(risk_score)
        
        # Construct the complete response
        result = {
            'customerInfo': {
                'customerId': profile_data['customerId'],
                'customerName': profile_data['customerName'],
                'accountAge': profile_data['accountAge'],
                'creditScore': profile_data['creditScore']
            },
            'riskAssessment': {
                'riskScore': risk_score,
                'riskCategory': risk_category
            },
            'transactionCount': len(profile_data['transactions']),
            'suspiciousActivityCount': len(profile_data['suspiciousActivities'])
        }

        return jsonify(result)
            
    except Exception as e:
        app.logger.error(f"Error retrieving customer profile: {str(e)}")
        return jsonify({"error": str(e)}), 500

    

def calculate_risk_score(profile):
    score = 0
    
    # Factor 1: Credit score
    if profile['creditScore'] < 600:
        score += 25
    elif profile['creditScore'] < 700:
        score += 15
    elif profile['creditScore'] < 750:
        score += 5
    
    # Factor 2: Account age
    if profile['accountAge'] < 12:
        score += 20
    elif profile['accountAge'] < 24:
        score += 10
    elif profile['accountAge'] < 36:
        score += 5
    
    # Factor 3: Suspicious activities
    if 'suspiciousActivities' in profile and profile['suspiciousActivities']:
        for activity in profile['suspiciousActivities']:
            score += activity['severity'] * 5
    
    # Factor 4: Foreign transactions
    foreign_tx_count = 0
    if 'transactions' in profile and profile['transactions']:
        for tx in profile['transactions']:
            if tx['country'] != 'USA':
                foreign_tx_count += 1
    
    if foreign_tx_count > 2:
        score += 15
    elif foreign_tx_count > 0:
        score += 10
    
    # Factor 5: Large deposits (over $10,000)
    large_deposits = 0
    if 'transactions' in profile and profile['transactions']:
        for tx in profile['transactions']:
            if tx['type'] == 'DEPOSIT' and tx['amount'] > 10000:
                large_deposits += 1
    
    if large_deposits > 1:
        score += 15
    elif large_deposits == 1:
        score += 8
    
    # Factor 6: Transaction velocity (high number of transactions)
    if 'transactions' in profile and profile['transactions']:
        tx_count = len(profile['transactions'])
        if tx_count > 20:
            score += 10
        elif tx_count > 10:
            score += 5
    
    # Cap the score at 100
    return min(score, 100)

def get_risk_category(score):
    """Determine risk category based on numerical score"""
    if score < 20:
        return "Low Risk"
    elif score < 50:
        return "Medium Risk"
    elif score < 75:
        return "High Risk"
    else:
        return "Extreme Risk"

    ########################## UTILITY FUNCTIONS ################################################

if __name__ == '__main__':
    app.run(debug=True)