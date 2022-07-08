from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api.auth.models import Token


class TokenHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return AnonymousUser(), None

        try:
            token_type, token = auth_header.split(' ')
        except ValueError:
            return AnonymousUser(), None

        if token_type != 'Bearer':
            return AnonymousUser(), None

        stored_token = Token.objects.filter(token=token).first()

        if stored_token is None:
            raise AuthenticationFailed('Token not found.')
        return (stored_token.user, stored_token.token)
