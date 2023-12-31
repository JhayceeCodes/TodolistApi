from rest_framework.authentication import BaseAuthentication
from authentication.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from authToken.tokens import decode_access_token


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Extract the token from the request (e.g., from headers, query parameters, or cookies)
        token = self.get_token_from_request(request)

        if not token:
            return None

        # Validate and decode the token
        user_id = self.decode_token(token)

        if user_id is None:
            return None

        # Fetch the user based on the user_id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(_('No such user'))

        # Return a tuple of (user, auth)
        return (user, None)

    def get_token_from_request(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]
            return token
        else:
            return None

    def decode_token(self, token):
        user_id = decode_access_token(token)
        if user_id is not None:
            return user_id
        return None
