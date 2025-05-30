"""
Basic API Example for API Lambda Router

This example demonstrates a simple REST API for managing users.
Deploy this to AWS Lambda with API Gateway integration.
"""

from api_lambda.router import route, api_handler
from api_lambda.request import HTTPRequest
from typing import Dict, Any, Union, Tuple


version: str = '1.0'

@route("/version", methods=["GET", "PATCH"])
def version_handler(request: HTTPRequest) -> Union[Dict[str, Any], Tuple[Dict[str, Any], int]]:
    """Version endpoint."""
    global version
    
    if request.method == 'GET':
        return {"version": version}
    elif request.method == 'PATCH':
        # Update version
        new_version: Union[str, Any] = request.body.get("new_version", '')
        if not new_version:
            return {"error": "Invalid version"}, 400
        
        if not isinstance(new_version, str):
            return {"error": "Invalid version"}, 400
        
        version = new_version
        
        return {"version": version}
    else:
        return {"error": "Invalid method"}, 405
    
    
def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    return api_handler(event, context, cors_enabled=True, cors_origin="*")