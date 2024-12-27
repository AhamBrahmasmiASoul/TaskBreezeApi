from typing import Optional, Any, Dict, Union

from rest_framework import serializers
from rest_framework.response import Response


def create_response(
        message: Optional[str] = None,
        data: Optional[Any] = None,
        status_code: int = 400
) -> Response:
    """Create a standardized response structure with optional fields."""
    response: Dict[str, Any] = {}
    if message:
        response["message"] = message
    if data:
        response["data"] = data
    return Response(response, status=status_code)

def custom_error_response(arg: Union[serializers.Serializer, str]):
    if isinstance(arg, serializers.Serializer):
        message = next(iter(next(iter(arg.errors.values()))))
    elif isinstance(arg, str):
        message = arg
    else:
        raise ValueError("Invalid argument type")
    return create_response(message=message)
