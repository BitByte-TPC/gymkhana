import uuid

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from api.clubs.models import Club

User = get_user_model()


class ListClubsViewTest(APITestCase):
    """Tests ListClubView for getting the list of clubs."""

    @pytest.mark.django_db
    def testListClubs_noClubExistsInDb_returnsEmptyList(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)
        # when
        response = self.client.get('/clubs/', format='json')
        # then
        self.assertEqual(len(response.data['results']), 0)

    @pytest.mark.django_db
    def testListClubs_oneClubExistsInDb_returnsOneClubInResponse(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)
        Club.objects.create(name="Bitbyte - The Programming Club",
                            category="S&T",
                            description="Aim to create thriving coding environment for developers.",
                            email="theprogclub@iiitdmj.ac.in <theprogclub@iiitdmj.ac.in>;",
                            logo="https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png")
        # when
        response = self.client.get('/clubs/', format='json')
        # then
        self.assertEqual(len(response.data['results']), 1)

    @pytest.mark.django_db
    def testListClubs_hundredClubExistsInDb_returnsFiftyClubInFirstResponse(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)
        for i in range(0, 100):
            Club.objects.create(name=uuid.uuid4(),
                                category="S&T",
                                description="some random string",
                                email=uuid.uuid4(),
                                logo="https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png")
        # when
        response = self.client.get('/clubs/', format='json')
        # then
        self.assertEqual(len(response.data['results']), 50)
