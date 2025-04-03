import requests
import json

# Flask API endpoint configuration
API_BASE_URL_1 = "http://127.0.0.1:5000/Client/check"  
API_BASE_URL_2 = "http://127.0.0.1:5000/Client/form" 
API_BASE_URL_3 = "http://127.0.0.1:5000/Client/loan" 
API_BASE_URL_4 = "http://127.0.0.1:5000/Client/loan-status" 

# Sample JSON data to send
json_data_1 = {
    "check_number" : 1,
    "bank_name" : "sg",
    "bank_address" :"test",
    "payer_name" : "ghassen",
    "payee_name" : "test",
    "amount" : 20000,
    "issue_date" : "test",
    "memo" : "test",
    "routing_number" : 1,
    "account_number": 1
}


json_data_2 = {
    "id" : "C1002",
    "nom" : "Smith",
    "prenom" :"John",
    "loan_type" : "commercial",
    "amount" : 20000,
    "description" : "testDescription"
}

json_data_3 = {
  "id": "C1002",
  "amount": 20000
}


# Headers to indicate we're sending JSON
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

headers2 = {
    "Accept": "application/json",
    # Add authentication if needed:
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

def make_get_request(url, headers):
    """Make a GET request to the API endpoint"""
    try:
        response = requests.get(
            url,
            headers=headers
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Return parsed JSON or raw response
        try:
            return response.json()
        except ValueError:
            return {
                "status_code": response.status_code,
                "content": response.text
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None)
        }


def make_post_request(url, data, headers):
    """Make a POST request to the API endpoint"""
    try:
        response = requests.post(
            url,
            data=json.dumps(data),  # Convert dict to JSON string
            headers=headers
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Try to parse JSON response
        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response", "status_code": response.status_code}
            
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}

if __name__ == "__main__":
    print(f"Sending POST request to: {API_BASE_URL_2}")
    print(f"Request data:\n{json.dumps(json_data_2, indent=2)}")
    
    result1 = make_post_request(API_BASE_URL_2, json_data_2, headers)
    
    print("\nResponse:")
    print(json.dumps(result1, indent=2))

    if result1:

        print(f"Sending POST request to: {API_BASE_URL_1}")
        print(f"Request data:\n{json.dumps(json_data_1, indent=2)}")
    
        result2 = make_post_request(API_BASE_URL_1, json_data_1, headers)
    
        print("\nResponse:")
        print(json.dumps(result2, indent=2))

        if result2:

            print(f"Sending POST request to: {API_BASE_URL_3}")
            print(f"Request data:\n{json.dumps(json_data_3, indent=2)}")
    
            result3 = make_post_request(API_BASE_URL_3, json_data_3, headers)
    
            print("\nResponse:")
            print(json.dumps(result3, indent=2))

            if result3:


                print(f"Sending GET request to: {API_BASE_URL_4}")
    
                result4 = make_get_request(API_BASE_URL_4, headers2)
    
                print("\nResponse:")
                print(json.dumps(result4, indent=2))


