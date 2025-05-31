# Basic Usage

Learn the core concepts and features of API Lambda Router.

## Route Definition

### Basic Routes

Use the `@route()` decorator to define endpoints:

```python
from api_lambda import route, HTTPRequest

@route("/health", methods="GET")
def health_check(request: HTTPRequest):
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
```

### Multiple HTTP Methods

A single function can handle multiple HTTP methods:

```python
@route("/items", methods=["GET", "POST"])
def handle_items(request: HTTPRequest):
    if request.method == 'POST':
        # Create new item
        return {"created": request.body, "id": "123"}, 201
    elif request.method == 'GET':
        return {"items": ["item1", "item2", "item3"]}
```

### Path Parameters

Extract dynamic values from URLs:

```python
# API Gateway style {param}
@route("/users/{user_id}", methods="GET")
def get_user(request: HTTPRequest):
    user_id = request.path["user_id"]
    return {"user_id": user_id, "name": f"User {user_id}"}

# Flask style <param> (automatically converted)
@route("/posts/<post_id>/comments/<comment_id>", methods="GET")
def get_comment(request: HTTPRequest):
    return {
        "post_id": request.path["post_id"],
        "comment_id": request.path["comment_id"]
    }
```

## Request Object

The `HTTPRequest` object provides structured access to request data:

```python
def my_handler(request: HTTPRequest):
    # Request body (parsed JSON)
    body_data = request.body
    name = body_data.get("name", "Unknown")
    
    # Path parameters
    user_id = request.path.get("user_id")
    
    # Query parameters
    limit = request.query.get("limit", "10")
    
    # HTTP headers
    content_type = request.headers.get("Content-Type")
    
    # Authorization context (from API Gateway)
    user_context = request.context.get("user")
    
    # HTTP method
    method = request.method
    
    return {
        "method": method,
        "user_id": user_id,
        "name": name,
        "limit": limit
    }
```

### Request Properties

| Property | Type | Description |
|----------|------|-------------|
| `body` | `Dict[str, Any]` | Parsed JSON request body |
| `path` | `Dict[str, str]` | URL path parameters |
| `query` | `Dict[str, str]` | Query string parameters |
| `headers` | `Dict[str, str]` | HTTP headers |
| `context` | `Dict[str, Any]` | Authorization context |
| `method` | `str` | HTTP method (GET, POST, etc.) |

## Response Handling

### Simple Responses

Return a dictionary for 200 OK responses:

```python
@route("/simple", methods="GET")
def simple_response(request: HTTPRequest):
    return {"message": "Success", "data": [1, 2, 3]}
```

### Custom Status Codes

Return a tuple with `(body, status_code)`:

```python
@route("/users", methods="POST")
def create_user(request: HTTPRequest):
    # Validate request
    if not request.body.get("name"):
        return {"error": "Name is required"}, 400
    
    # Create user
    user = {"id": "123", "name": request.body["name"]}
    return user, 201

@route("/users/{user_id}", methods="DELETE")
def delete_user(request: HTTPRequest):
    user_id = request.path["user_id"]
    # Delete logic here...
    return {"message": f"User {user_id} deleted"}, 204
```

## CORS Support

Enable CORS for web browser requests:

```python
def lambda_handler(event, context):
    return api_handler(
        event, 
        context,
        cors_enabled=True,           # Enable CORS
        cors_origin="*"              # Allow all origins (or specify domain)
    )
```

For production, specify allowed origins:

```python
def lambda_handler(event, context):
    return api_handler(
        event, 
        context,
        cors_enabled=True,
        cors_origin="https://myapp.com"  # Only allow your domain
    )
```

## Error Handling

### Automatic Error Responses

The framework automatically handles common errors:

```python
# 404 Not Found - when no route matches
# 500 Internal Server Error - when handler throws exception
```

### Custom Error Responses

Create custom error response formats:

```python
def custom_error_factory(status_code: int, message: str, error_code: str):
    return {
        "success": False,
        "error": {
            "message": message,
            "code": error_code,
            "status": status_code,
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

### Debug Mode

Enable debug mode for development:

```python
def lambda_handler(event, context):
    return api_handler(
        event, 
        context,
        debug_mode=True  # Includes stack traces in error responses
    )
```

## Complete Example

Here's a complete CRUD API example:

```python
from api_lambda import route, api_handler, HTTPRequest

# In-memory storage (use a database in production)
users = {
    "1": {"id": "1", "name": "John Doe", "email": "john@example.com"},
    "2": {"id": "2", "name": "Jane Smith", "email": "jane@example.com"}
}

@route("/users", methods="GET")
def list_users(request: HTTPRequest):
    """List all users."""
    return {"users": list(users.values())}

@route("/users", methods="POST")
def create_user(request: HTTPRequest):
    """Create a new user."""
    if not request.body.get("name") or not request.body.get("email"):
        return {"error": "Name and email are required"}, 400
    
    user_id = str(len(users) + 1)
    user = {
        "id": user_id,
        "name": request.body["name"],
        "email": request.body["email"]
    }
    users[user_id] = user
    return user, 201

@route("/users/{user_id}", methods="GET")
def get_user(request: HTTPRequest):
    """Get a specific user."""
    user_id = request.path["user_id"]
    if user_id not in users:
        return {"error": "User not found"}, 404
    return users[user_id]

@route("/users/{user_id}", methods="PUT")
def update_user(request: HTTPRequest):
    """Update a user."""
    user_id = request.path["user_id"]
    if user_id not in users:
        return {"error": "User not found"}, 404
    
    user = users[user_id]
    user.update(request.body)
    return user

@route("/users/{user_id}", methods="DELETE")
def delete_user(request: HTTPRequest):
    """Delete a user."""
    user_id = request.path["user_id"]
    if user_id not in users:
        return {"error": "User not found"}, 404
    
    del users[user_id]
    return {"message": "User deleted successfully"}

def lambda_handler(event, context):
    return api_handler(event, context, cors_enabled=True, debug_mode=True)
```
