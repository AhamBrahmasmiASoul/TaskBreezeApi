from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rajneehsoulapiapp.authenticate_user import SocialAuthentication, TokenAuthentication


def _authenticate_with_token(request):
    """Attempts token authentication and checks for token expiry."""
    try:
        user_auth_tuple = TokenAuthentication().authenticate(request)
        if user_auth_tuple is None:
            raise AuthenticationFailed('Invalid token')

        user, auth_token = user_auth_tuple  # Extract user and token

        # Check if the token has expired
        if auth_token.expires_at < timezone.now():
            raise AuthenticationFailed('Token has expired')

        return user, auth_token  # Return authenticated user and valid token

    except AuthenticationFailed as e:
        raise AuthenticationFailed(f'Token authentication failed: {str(e)}')


def _authenticate_with_social_or_token(request):
    """Attempts social authentication first, then falls back to token authentication."""
    try:
        return SocialAuthentication().authenticate(request)  # Try social authentication
    except AuthenticationFailed as e:
        # If social authentication fails, attempt regular token authentication
        return _authenticate_with_token(request)


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')

        # Check if the Authorization header is present
        if not auth_header:
            raise AuthenticationFailed('Authorization header missing')

        # Case 1: Bearer token-based authentication
        if auth_header.startswith('Bearer '):
            return _authenticate_with_social_or_token(request)

        # Case 2: Token-based without Bearer (for regular TokenAuthentication check)
        return _authenticate_with_token(request)

    def authenticate_header(self, request):
        """
        Returns the `WWW-Authenticate` header for unauthenticated requests.
        """
        return 'Bearer'

