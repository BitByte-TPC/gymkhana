import uuid
from unittest import mock
from uuid import UUID

import pytest
from django.contrib.auth import get_user_model
from google.auth.exceptions import GoogleAuthError
from rest_framework import status
from rest_framework.test import APITestCase

from api.auth.models import Token


class TokenViewTest(APITestCase):
    """Tests TokenView for creating and revoking access tokens."""

    User = get_user_model()

    @pytest.mark.django_db
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_userDoesNotExist_createsNewUser_returnsTokenAndUserInfo(
            self, mock_verify_token):
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
            'picture': 'http://picture_url',
        }

        response = self.client.post('/auth/token/', {'id_token': 'some_id_token'}, format='json')

        created_user = self.User.objects.filter(email='test@user.com').first()
        token = created_user.token

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['user'], {
            'email': 'test@user.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
        })
        self.assertIsNotNone(created_user)
        self.assertIsNotNone(token)
        self.assertIsInstance(UUID(token.token), UUID)

    @pytest.mark.django_db
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_userExists_tokenDoesNotExist_createsTokenAndReturnsWithUserInfo(
            self, mock_verify_token):
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
        }
        user = self.User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')

        response = self.client.post('/auth/token/', {'id_token': 'some_id_token'}, format='json')

        token = Token.objects.filter(user=user).first()
        number_of_users_in_db = self.User.objects.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['user'], {
            'email': 'test@user.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
        })
        self.assertEqual(number_of_users_in_db, 1,
                         f'Got {number_of_users_in_db} of users in db, expected 1')
        self.assertIsNotNone(token)
        self.assertIsInstance(UUID(token.token), UUID)

    @pytest.mark.django_db
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_tokenExists_returnsExistingTokenWithUserInfo(
            self, mock_verify_token):
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
        }
        existing_user = self.User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        existing_token = Token.objects.create(token=uuid.uuid4().hex, user=existing_user)

        response = self.client.post('/auth/token/', {'id_token': 'some_id_token'}, format='json')

        tokens_count = Token.objects.count()
        users_count = self.User.objects.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data['user'], {
            'email': 'test@user.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
        })

        self.assertEqual(tokens_count, 1,
                         f'Got {tokens_count} tokens in db, expected 1')
        self.assertEqual(users_count, 1,
                         f'Got {users_count} users in db, expected 1')
        self.assertEqual(response.data['token'], existing_token.token)

    @pytest.mark.django_db
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_invalidIdToken_throwsForbiddenError(
            self, mock_verify_token):
        mock_verify_token.side_effect = ValueError()

        response = self.client.post('/auth/token/', {'id_token': 'some_id_token'}, format='json')

        tokens_count = Token.objects.count()
        users_count = self.User.objects.count()
        self.assertEqual(tokens_count, 0, f'Got {tokens_count} tokens, expected to be 0')

        self.assertEqual(users_count, 0,
                         f'Got {users_count} users, expected 0')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['message'],
            'Token could not be validated. Please try again.')

    @pytest.mark.django_db
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_invalidTokenIssuer_throwsBadRequestError(
            self, mock_verify_token):
        mock_verify_token.side_effect = GoogleAuthError()

        response = self.client.post('/auth/token/', {'id_token': 'some_id_token'}, format='json')

        tokens_count = Token.objects.count()
        users_count = self.User.objects.count()
        self.assertEqual(tokens_count, 0, f'Got {tokens_count} tokens, expected to be 0')

        self.assertEqual(users_count, 0,
                         f'Got {users_count} users, expected 0')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'],
            'Invalid token issuer. Try again with correct token.')
