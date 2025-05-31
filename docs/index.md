# API Lambda Router

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/abdulkarim-essam/api-lambda/ci.yml?branch=main)](https://github.com/abdulkarim-essam/api-lambda/actions)
[![Coverage](https://img.shields.io/codecov/c/github/abdulkarim-essam/api-lambda)](https://codecov.io/gh/abdulkarim-essam/api-lambda)

A lightweight, Flask-inspired routing framework for AWS Lambda functions with API Gateway integration. Build serverless APIs with clean, decorative routing and automatic request/response handling.

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

### Basic Example

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

## Architecture

This library is specifically designed for AWS Lambda + API Gateway:

```
Internet → API Gateway → Lambda Function → Your Routes
```
## Support

- **GitHub**: [Issues & Discussions](https://github.com/abdulkarim-essam/api-lambda/issues)
- **Email**: abdulkarim.essam@hotmail.com

---

**Made with ❤️ for the serverless community**