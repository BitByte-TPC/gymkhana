import logging
from typing import Dict, Mapping

from django.contrib.auth import get_user_model
from google.auth.exceptions import GoogleAuthError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.models import Token
from common.clients.google import google_client

from .serializers import (CreateTokenRequestSerializer,
                          CreateTokenResponseSerializer)


class TokenView(APIView):
    """View to create and revoke the tokens."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateTokenRequestSerializer(data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data.get('authorization_code')
            try:
                auth_response = google_client.exchange_auth_code_for_token(code)
            except Exception:
                logging.exception('Error while exchanging auth code for token')
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={'message': 'Invalid authorization code. Try logging in again.'})
            try:
                id_info = google_client.verify_id_token(auth_response.get('id_token'))
            except ValueError:
                logging.exception('Error while verifying the token')
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
            access_token = Token.if_expired_get_new(access_token, user)
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


class DeleteTokenView(APIView):
    """View to delete the tokens."""

    def delete(self, request):
        token = Token.objects.filter(user=request.user).first()
        if token:
            token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
