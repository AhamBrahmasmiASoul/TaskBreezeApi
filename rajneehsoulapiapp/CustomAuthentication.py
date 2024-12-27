from rest_framework.exceptions import AuthenticationFailed
from rajneehsoulapiapp.authenticate_user import SocialAuthentication, TokenAuthentication  # Ensure this is a class

class CustomAuthentication:
    @staticmethod
    def authenticate(request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')

        # Check if the Authorization header is present
        if not auth_header:
            raise AuthenticationFailed('Authorization required')

        # Case 1: Bearer token-based authentication
        if auth_header.startswith('Bearer '):
            return CustomAuthentication._authenticate_with_social_or_token(request)

        # Case 2: Token-based without Bearer (for SocialAuthentication check)
        # If not a Bearer token, attempt regular token authentication
        return CustomAuthentication._authenticate_with_token(request)

    @staticmethod
    def _authenticate_with_token(request):
        """Attempts token authentication"""
        try:
            # Use TokenAuthentication to authenticate the request
            return TokenAuthentication().authenticate(request)
        except AuthenticationFailed:
            # If token authentication fails, raise an error
            raise AuthenticationFailed('Token authentication failed')

    @staticmethod
    def _authenticate_with_social_or_token(request):
        """Attempts social authentication first, then falls back to token authentication"""
        try:
            # Try Social Authentication
            return SocialAuthentication().authenticate(request)
        except AuthenticationFailed:
            raise AuthenticationFailed('Token authentication failed')
