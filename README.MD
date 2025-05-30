# API Lambda Router 

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/abdulkarim-essam/api-lambda/ci.yml?branch=main)](https://github.com/abdulkarim-essam/api-lambda/actions)
[![Coverage](https://img.shields.io/codecov/c/github/abdulkarim-essam/api-lambda)](https://codecov.io/gh/abdulkarim-essam/api-lambda)

A lightweight, Flask-inspired routing framework for AWS Lambda functions with API Gateway integration. Build serverless APIs with clean, decorative routing and automatic request/response handling.


## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [License](#license)

## Features

- **Flask-style Decorative Routing** - Clean `@route()` decorators for endpoint definition

- **Simple Request/Response Handling** - JSON parsing, CORS, error handling out of the box

- **Dynamic Path Parameters** - Support for both `{id}` and `<id>` parameter styles

- **Zero Dependencies** - Pure Python, no external packages required

- **Type Safety** - Full type hints and protocol definitions

- **CORS Support** - Built-in CORS handling for web applications

- **Debug Mode** - Detailed error tracebacks for development

- **Customizable Errors** - Custom error response factories

## Quick Start

### Installation

```bash
pip install api-lambda-router
```

### Basic Usage

```python
from api_lambda import route, api_handler, HTTPRequest

@route("/hello", methods="GET")
def hello_world(request: HTTPRequest):
    return {"message": "Hello, World!"}

@route("/users/{user_id}", methods=["GET", "PUT"])
def handle_user(request: HTTPRequest):
    user_id = request.path["user_id"]
    
    if request.body.get("name"):
        # PUT - Update user
        return {"user_id": user_id, "name": request.body["name"]}, 200
    else:
        # GET - Retrieve user
        return {"user_id": user_id, "name": "John Doe"}

# AWS Lambda handler
def lambda_handler(event, context):
    return api_handler(event, context, cors_enabled=True, debug_mode=True)
```

### Deploy to AWS

```bash
# Package your function
zip -r function.zip .

# Deploy using AWS CLI
aws lambda create-function \
    --function-name my-api \
    --runtime python3.9 \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip
```

## 📖 Documentation

### Route Definition

Define routes using the `@route()` decorator:

```python
from api_lambda import route, HTTPRequest

# Simple GET route
@route("/health")
def health_check(request: HTTPRequest):
    return {"status": "healthy"}

# Multiple HTTP methods
@route("/items", methods=["GET", "POST"])
def handle_items(request: HTTPRequest):
    if request.body:  # POST request
        return {"created": request.body}, 201
    else:  # GET request
        return {"items": ["item1", "item2"]}

# Dynamic path parameters
@route("/items/{item_id}/comments/{comment_id}")
def get_comment(request: HTTPRequest):
    return {
        "item_id": request.path["item_id"],
        "comment_id": request.path["comment_id"]
    }
```

### Request Object

The `HTTPRequest` object provides structured access to request data:

```python
def my_handler(request: HTTPRequest):
    # Access different request components
    body_data = request.body          # Parsed JSON body
    path_params = request.path        # URL path parameters
    query_params = request.query      # Query string parameters
    headers = request.headers         # HTTP headers
    auth_context = request.context    # Authorization context
```

### Response Handling

Return responses in multiple formats:

```python
# Simple dict response (200 status)
return {"message": "Success"}

# Tuple with status code
return {"error": "Not found"}, 404
```

### Error Handling

Customize error responses:

```python
def custom_error_factory(status_code: int, message: str, error_code: str):
    return {
        "success": False,
        "error": {
            "message": message,
            "code": error_code,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    }

def lambda_handler(event, context):
    return api_handler(
        event, 
        context,
        custom_error_factory=custom_error_factory
    )
```

## Architecture

### AWS Integration

This library is specifically designed for AWS Lambda + API Gateway:

```
Internet → API Gateway → Lambda Function → Your Routes
```

### Request Flow

1. **API Gateway** receives HTTP request
2. **Lambda** invokes your handler with event/context
3. **Router** matches path and method to registered routes
4. **Handler** processes request and returns response
5. **Response** automatically formatted for API Gateway

### Performance Considerations

- **Cold Start Optimization**: Minimal imports and lazy loading
- **Memory Efficient**: No heavy dependencies or global state
- **Fast Routing**: Efficient path matching with parameter extraction

## Testing

Run the test suite:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=api_lambda --cov-report=html
```

## Examples

Check out the [examples/](examples/) directory for complete working examples:

- **Basic API** - Simple CRUD operations
- **Authentication** - JWT token handling
- **File Upload** - Binary data processing
- **Database Integration** - DynamoDB operations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Flask's elegant routing system
- Built for the AWS serverless ecosystem
- Designed with developer experience in mind

## Contact

- **GitHub**: [@abdulkarim-essam](https://github.com/abdulkarim-essam)
- **LinkedIn**: [Abdulkarim Essam](https://linkedin.com/in/abdulkarim-essam)
- **Email**: abdulkarim.essam@hotmail.com

---

**Made with ❤️ for the serverless community**