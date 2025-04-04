# Microservices Project

This project consists of **4 microservices** that communicate with each other to handle loan requests and financial operations. Each microservice is built using a different technology stack:

- **REST Microservice**: Developed using Flask (Python).
- **SOAP Microservice**: A Java application deployed on an Axis2 server.
- **GraphQL Microservice**: Developed using Node.js.
- **gRPC Microservice**: Developed using Python.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.9 or higher
- Node.js (v16 or higher)
- Maven (for building the SOAP service)
- Axis2 server (for deploying the SOAP service)
- Virtual environment tools for Python (`venv` or `virtualenv`)

---

## How to Run the Project

To run this project locally, start each microservice separately as described below:

### 1. Running the REST Microservice

The REST microservice handles loan requests and integrates with other services.

```bash
cd load_request_service_rest

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the service
python app.py
```

- The REST service will run on `http://localhost:5000` with debug mode enabled.

---

### 2. Running the GraphQL Microservice

The GraphQL microservice manages customer data and financial transactions.

```bash
cd bank-service

# Install dependencies
npm install

# Start the service
node server.js
```

- The GraphQL service will run on `http://localhost:4000`.

---

### 3. Running the gRPC Microservice

The gRPC microservice handles money retrieval operations.

```bash
cd provider

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install grpcio grpcio-tools

# Start the service
python server.py
```

- The gRPC service will run on `http://localhost:50051`.

---

### 4. Running the SOAP Microservice

The SOAP microservice retrieves customer financial profiles for risk assessment.

```bash
cd partner-service/finriskService

# Build the project using Maven
mvn clean install 

# Deploy the service to the Axis2 server
cp target/customer-financial-profile-service.aar $AXIS2_HOME/repository/services/

# Start the Axis2 server
cd $AXIS2_HOME/bin
./axis2Service.sh
```

- The SOAP service will be accessible on `http://localhost:8080`.

---

## Project Structure

Here is an overview of the project structure:

```
├── load_request_service_rest/   # REST microservice
├── bank-service/                # GraphQL microservice
├── provider/                    # gRPC microservice
├── partner-service/             # SOAP microservice
├── README.md                    # Documentation
├── .gitignore                   # Git ignore rules
```

---

## Testing the Services

### REST API Endpoints

- **Submit Loan Form**: `POST /Client/form`
- **Submit Check**: `POST /Client/check`
- **Execute Loan**: `POST /Client/loan`
- **Check Loan Status**: `GET /Client/loan-status`

### GraphQL Endpoints

- **Check Validity**: `POST /check`
- **Add Amount to Customer**: `POST /customer/id`

### gRPC Service

- **Retrieve Money**: `RetrieveMoney` method on port `50051`.

### SOAP Service

- **Get Customer Financial Profile**: Accessible via the Axis2 server.

---

## Notes

- Ensure all services are running before testing the integration.
- Update the environment variables in the code if needed (e.g., `SOAP_ENDPOINT`, `NODE_APP_URL`).
- Use tools like Postman, GraphiQL, or gRPC clients to test the APIs.

---

## License

This project is licensed under the MIT License.

