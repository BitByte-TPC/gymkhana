import functools
import os
import pytest
import sys
from django.conf import settings
from django.urls.base import clear_url_caches
from importlib import import_module, reload
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock


def reload_root_urls(wrapped):

    @functools.wraps(wrapped)
    def wrapper(*args, **kwargs):
        clear_url_caches()
        if settings.ROOT_URLCONF in sys.modules:
            reload(sys.modules[settings.ROOT_URLCONF])
        else:
            import_module(settings.ROOT_URLCONF)

        return wrapped(*args, **kwargs)

    return wrapper


class AdminEndpointTest(APITestCase):

    @pytest.mark.order(1)
    @mock.patch.dict(os.environ, {'ENV': 'dev'})
    @reload_root_urls
    def testAdminEndpoint_inDevEnv_returns200Ok(self):
        """Tests the /admin/ endpoint to return status code 200 when env is dev"""
        url = '/admin/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.order(2)
    @reload_root_urls
    def testAdminEndpoint_notInDevEnv_returns404(self):
        """Tests the /admin/ endpoint to return status code 404 when env is not dev"""
        url = '/admin/'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @pytest.mark.order(3)
    @reload_root_urls
    def test_dummy_toResetRootUrls(self):
        """Should always run at the end to reset the urlconf for default environment"""
        pass


class PingTest(APITestCase):
    def test_ping(self):
        """Tests the /ping/ endpoint to return message: 'Up'"""
        url = '/ping/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Up'})
