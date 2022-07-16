import uuid
from datetime import datetime, timezone
from unittest import mock
from uuid import UUID

import pytest
from django.contrib.auth import get_user_model
from google.auth.exceptions import GoogleAuthError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory, APITestCase

from api.auth.backend import TokenHeaderAuthentication
from api.auth.models import Token

User = get_user_model()


class TokenViewTest(APITestCase):
    """Tests TokenView for creating and revoking access tokens."""

    @pytest.mark.django_db
    @mock.patch('time.sleep')
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_userDoesNotExist_createsNewUser_returnsTokenAndUserInfo(
            self, mock_verify_token, mock_fetch_token, mock_sleep):
        # given
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
            'picture': 'http://picture_url',
        }
        mock_fetch_token.return_value = {
            'id_token': 'some-id-token'
        }

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        created_user = User.objects.filter(email='test@user.com').first()
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
    @mock.patch('time.sleep')
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_userExists_tokenDoesNotExist_createsTokenAndReturnsWithUserInfo(
            self, mock_verify_token, mock_fetch_token, mock_sleep):
        # given
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
        }
        mock_fetch_token.return_value = {
            'id_token': 'some-id-token'
        }

        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        token = Token.objects.filter(user=user).first()
        number_of_users_in_db = User.objects.count()

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
    @mock.patch('time.sleep')
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_tokenExists_returnsExistingTokenWithUserInfo(
            self, mock_verify_token, mock_fetch_token, mock_sleep):
        # given
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
        }
        mock_fetch_token.return_value = {
            'id_token': 'some-id-token'
        }

        existing_user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        existing_token = Token.objects.create(token=uuid.uuid4().hex, user=existing_user)

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        tokens_count = Token.objects.count()
        users_count = User.objects.count()

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
    @mock.patch('time.sleep')
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_expiredTokenExists_returnsNewTokenWithUserInfo(
            self, mock_verify_token, mock_fetch_token, mock_sleep):
        # given
        mock_verify_token.return_value = {
            'email': 'test@user.com',
            'given_name': 'Test',
            'family_name': 'User',
        }
        mock_fetch_token.return_value = {
            'id_token': 'some-id-token'
        }

        existing_user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        existing_token = Token.objects.create(token=uuid.uuid4().hex, user=existing_user)
        existing_token.created_at = datetime(2022, 7, 9, 10, 10, 10, 10, timezone.utc)
        existing_token.save()

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        tokens_count = Token.objects.count()
        users_count = User.objects.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tokens_count, 1,
                         f'Got {tokens_count} tokens in db, expected 1')
        self.assertEqual(users_count, 1,
                         f'Got {users_count} users in db, expected 1')
        self.assertNotEqual(response.data['token'], existing_token.token)

    @pytest.mark.django_db
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    def test_createToken_invalidAuthorizationCodeInRequest_throwsForbiddenError(
            self, mock_fetch_token):
        # given
        mock_fetch_token.side_effect = Exception()

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        tokens_count = Token.objects.count()
        users_count = User.objects.count()
        self.assertEqual(tokens_count, 0, f'Got {tokens_count} tokens, expected to be 0')

        self.assertEqual(users_count, 0,
                         f'Got {users_count} users, expected 0')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @pytest.mark.django_db
    @mock.patch('time.sleep')
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_invalidIdToken_throwsForbiddenError(
            self, mock_verify_token, mock_fetch_token, mock_sleep):
        # given
        mock_verify_token.side_effect = ValueError()
        mock_fetch_token.return_value = {
            'id_token': 'some-id-token'
        }

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        tokens_count = Token.objects.count()
        users_count = User.objects.count()
        self.assertEqual(tokens_count, 0, f'Got {tokens_count} tokens, expected to be 0')

        self.assertEqual(users_count, 0,
                         f'Got {users_count} users, expected 0')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['message'],
            'Token could not be validated. Please try again.')

    @pytest.mark.django_db
    @mock.patch('time.sleep')
    @mock.patch('google_auth_oauthlib.flow.Flow.fetch_token')
    @mock.patch('google.oauth2.id_token.verify_oauth2_token')
    def test_createToken_invalidTokenIssuer_throwsBadRequestError(
            self, mock_verify_token, mock_fetch_token, mock_sleep):
        # given
        mock_verify_token.side_effect = GoogleAuthError()
        mock_fetch_token.return_value = {
            'id_token': 'some-id-token'
        }

        # when
        response = self.client.post(
            '/auth/token/', {'authorization_code': 'some-code'},
            format='json')

        # then
        tokens_count = Token.objects.count()
        users_count = User.objects.count()
        self.assertEqual(tokens_count, 0, f'Got {tokens_count} tokens, expected to be 0')

        self.assertEqual(users_count, 0,
                         f'Got {users_count} users, expected 0')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'],
            'Invalid token issuer. Try again with correct token.')


class TokenHeaderAuthenticationTest(APITestCase):
    """Tests Custom authentication backend: TokenHeaderAuthentication."""
    backend = TokenHeaderAuthentication()
    request_factory = APIRequestFactory()

    def test_authenticate_noAuthHeaderPresentInRequest_returnsAnonymousUser(self):
        # given
        request = self.request_factory.get('/some/path')

        # when
        user, _ = self.backend.authenticate(request)

        # then
        self.assertTrue(user.is_anonymous, "Should return anonymous user if no auth header")

    def test_authenticate_invalidAuthHeaderPresentInRequest_returnsAnonymousUser(self):
        # given
        request = self.request_factory.get(
            '/some/path', HTTP_AUTHORIZATION='Helo')

        # when
        user, _ = self.backend.authenticate(request)

        # then
        self.assertTrue(user.is_anonymous, "Should return anonymous user if invalid auth header")

    def test_authenticate_invalidTokenPrefix_returnsAnonymousUser(self):
        # given
        request = self.request_factory.get(
            '/some/path', HTTP_AUTHORIZATION='InvalidPrefix sljdfls')

        # when
        user, _ = self.backend.authenticate(request)

        # then
        self.assertTrue(user.is_anonymous,
                        "Should return anonymous user if invalid prefix in auth header")

    @pytest.mark.django_db
    def test_authenticate_tokenDoesNotExist_throwsAuthenticationFailedException(self):
        # given
        request = self.request_factory.get(
            '/some/path', HTTP_AUTHORIZATION='Bearer sometoken')

        # when/then
        self.assertRaises(AuthenticationFailed, self.backend.authenticate, request)

    @pytest.mark.django_db
    def test_authenticate_validToken_returnsRealUser(self):
        # given
        created_user = User.objects.create(email='email@a.b')
        created_token = Token.objects.create(token='sometokenvalue', user=created_user)
        request = self.request_factory.get('/some/path', HTTP_AUTHORIZATION='Bearer sometokenvalue')

        # when
        authenticated_user, token = self.backend.authenticate(request)

        # then
        self.assertTrue(authenticated_user.is_active,
                        "Should return active user if token is valid")
        self.assertEqual(authenticated_user.email, created_user.email)
        self.assertEqual(token, created_token.token)


class DeleteTokenViewTest(APITestCase):
    """Test DeleteTokenView to delete token"""

    @pytest.mark.django_db
    def test_deleteToken_tokenDoesNotExists_returnHTTPNoContent(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)
        # when
        response = self.client.delete(
            '/auth/token:revoke/')
        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @pytest.mark.django_db
    def test_deleteToken_tokenExist_returnHTTPNoContent(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        Token.objects.create(token=uuid.uuid4().hex, user=user)
        self.client.force_authenticate(user)
        # when
        response = self.client.delete('/auth/token:revoke/')
        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
