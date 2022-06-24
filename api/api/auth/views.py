from typing import Dict, Mapping

from django.contrib.auth import get_user_model
from google.auth.exceptions import GoogleAuthError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.models import Token
from common.clients.google import google_client

from .serializers import (CreateTokenRequestSerializer,
                          CreateTokenResponseSerializer)


class TokenView(APIView):
    """View to create and revoke the tokens."""

    def post(self, request):
        serializer = CreateTokenRequestSerializer(data=request.data)

        if serializer.is_valid():
            try:
                id_info = google_client.verify_id_token(
                    serializer.validated_data.get('id_token'))
            except ValueError:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={'message': 'Token could not be validated. Please try again.'})
            except GoogleAuthError:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': 'Invalid token issuer. Try again with correct token.'}
                )

            user_info = self._extract_userdata_from_id_token(id_info)

            user = self._find_or_create_user(user_info)
            access_token = Token.find_or_create(user)

            return Response(data=CreateTokenResponseSerializer(access_token).data)

    def _extract_userdata_from_id_token(self, validated_id_info: Mapping[str, str]) -> Dict:
        return {
            'email': validated_id_info.get('email'),
            'first_name': validated_id_info.get('given_name'),
            'last_name': validated_id_info.get('family_name'),
            'picture_url': validated_id_info.get('picture'),
        }

    def _find_or_create_user(self, user_info):
        user = get_user_model().objects.filter(email=user_info.get('email')).first()

        if not user:
            user = get_user_model().objects.create(
                email=user_info.get('email'),
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'))
        return user
