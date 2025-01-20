from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rajneehsoulapiapp.authenticate_user import SocialAuthentication, TokenAuthentication

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')

        # Check if the Authorization header is present
        if not auth_header:
            raise AuthenticationFailed('Authorization required')

        # Case 1: Bearer token-based authentication
        if auth_header.startswith('Bearer '):
            return self._authenticate_with_social_or_token(request)

        # Case 2: Token-based without Bearer (for SocialAuthentication check)
        # If not a Bearer token, attempt regular token authentication
        return self._authenticate_with_token(request)

    def authenticate_header(self, request):
        """
        Returns the `WWW-Authenticate` header for unauthenticated requests.
        """
        return 'Bearer'

    def _authenticate_with_token(self, request):
        """Attempts token authentication."""
        try:
            # Use TokenAuthentication to authenticate the request
            return TokenAuthentication().authenticate(request)
        except AuthenticationFailed:
            # If token authentication fails, raise an error
            raise AuthenticationFailed('Token authentication failed')

    def _authenticate_with_social_or_token(self, request):
        """Attempts social authentication first, then falls back to token authentication."""
        try:
            # Try Social Authentication
            return SocialAuthentication().authenticate(request)
        except AuthenticationFailed:
            raise AuthenticationFailed('Token authentication failed')
