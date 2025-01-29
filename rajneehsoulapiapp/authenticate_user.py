import requests
from django.urls import reverse
from drf_social_oauth2.authentication import validator
from drf_social_oauth2.oauth2_endpoints import AccessToken
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from social_core.exceptions import MissingBackend, AuthException
from social_django.utils import load_strategy, load_backend
from social_django.views import NAMESPACE

from rajneehsoulapiapp.login.models import AuthToken, EmailIdRegistration, CustomUser
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get token from the request header
        token = request.META.get('HTTP_AUTHORIZATION', '')

        if not token:
            logger.error("No token provided in request header.")
            return None  # No token provided, so skip to next authentication step

        try:
            # Get the AuthToken instance using the token
            token_instance = AuthToken.objects.get(key=token)
            logger.info(f"Token found: {token_instance.key}")

            # Get the corresponding MobileRegistration instance
            email_id_registration = EmailIdRegistration.objects.get(id=token_instance.user.id)
            logger.info(f"MobileRegistration found for user ID {email_id_registration.id}")

            # Fetch the associated CustomUser object from MobileRegistration via the userMobileLinked field
            print("email_id_registration.id: ", email_id_registration.id)
            user = CustomUser.objects.get(userMobileLinked=email_id_registration.id)
            logger.info(f"CustomUser found for user ID {user.id}")

        except (AuthToken.DoesNotExist, EmailIdRegistration.DoesNotExist, CustomUser.DoesNotExist) as e:
            print("exception -------------> ", str(e))
            logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed('Invalid token or user does not exist')

        # Return the CustomUser instance (which has 'is_authenticated')
        return user, token_instance  # Now you return the CustomUser, not MobileRegistration


from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from oauth2_provider.models import AccessToken
from django.utils.timezone import now

class SocialAuthentication(BaseAuthentication):
    """
    Custom authentication class to validate social OAuth tokens.
    """

    def authenticate(self, request):
        """
        Extract and validate the token from the request.
        """
        # Extract the Authorization header
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            raise AuthenticationFailed('Invalid token header. No credentials provided.')

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. Token missing.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token contains spaces.')

        # Extract the token and validate
        token = auth[1]
        user = self.validate_access_token(token.decode('utf-8'))
        return user, token

    @staticmethod
    def validate_access_token(token):
        """
        Validate the access token using Django OAuth Toolkit.
        """
        try:
            # Query the AccessToken model for the provided token
            access_token = AccessToken.objects.get(token=token)

            # Check if the token has expired
            if access_token.is_expired():
                raise AuthenticationFailed("Access token has expired.")

            # Return the user associated with the token
            return access_token.user
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed("Invalid access token.")

