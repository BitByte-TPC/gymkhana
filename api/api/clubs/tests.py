from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from api.clubs.models import Club

User = get_user_model()


class ListClubsViewTest(APITestCase):
    """Tests ListClubView for getting the list of clubs."""

    def testListClubs_noClubExistsInDb_returnsEmptyList(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)
        # when
        response = self.client.get('/clubs/', format='json')
        # then
        self.assertEqual(Club.objects.count(), len(response.data))

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
        self.assertEqual(Club.objects.count(), len(response.data))
