from datetime import timedelta

from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the result from the default JWT Authentication
        result = super().authenticate(request)

        if result is not None:
            user, token = result
            # Check if the user has been inactive for more than 5 minutes
            if user.last_api_call and now() - user.last_api_call > timedelta(minutes=30):
                raise AuthenticationFailed("Token is invalid or expired")

        return result
