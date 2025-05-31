# Getting Started

This guide will help you create your first API using API Lambda Router.

## Prerequisites

- Python 3.8 or higher
- AWS account (for deployment)
- Basic understanding of AWS Lambda and API Gateway

## Installation

Install the package from PyPI:

```bash
pip install api-lambda-router
```

or download the source code and add to your project manually.

## Creating Your First API

### Step 1: Create a Lambda Function

Create a new file called `lambda_function.py`:

```python
from api_lambda import route, api_handler, HTTPRequest

@route("/hello", methods="GET")
def hello_world(request: HTTPRequest):
    """Simple hello world endpoint."""
    return {"message": "Hello, World!", "status": "success"}

@route("/echo", methods="POST")
def echo_message(request: HTTPRequest):
    """Echo back the request body."""
    message = request.body.get("message", "No message provided")
    return {"echo": message}

@route("/users/{user_id}", methods="GET")
def get_user(request: HTTPRequest):
    """Get user by ID from path parameter."""
    user_id = request.path["user_id"]
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }

# Lambda handler function
def lambda_handler(event, context):
    return api_handler(
        event, 
        context, 
        cors_enabled=True,  # Enable CORS for web requests
        debug_mode=True     # Include stack traces in errors (disable in production)
    )
```

### Step 2: Test Locally

You can test your routes locally by creating a mock event:

```python
# test_local.py
from lambda_function import lambda_handler

def test_hello():
    event = {
        "httpMethod": "GET",
        "path": "/hello",
        "body": None,
        "queryStringParameters": None,
        "headers": {},
        "requestContext": {}
    }
    
    response = lambda_handler(event, {})
    print(f"Status: {response['statusCode']}")
    print(f"Body: {response['body']}")

if __name__ == "__main__":
    test_hello()
```

Run the test:

```bash
python test_local.py
```
