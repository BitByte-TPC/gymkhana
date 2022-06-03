from rest_framework import status
from rest_framework.test import APITestCase


class PingTest(APITestCase):
    def test_ping(self):
        """Tests the /ping/ endpoint to return message: 'Up'"""
        url = '/ping/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Up'})
