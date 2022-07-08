from rest_framework.test import APITestCase

from api.clubs.models import Club


class ListClubsViewTest(APITestCase):
    """Tests ListClubView for getting the list of clubs."""

    def testListClubs_noClubExistsInDb_returnsEmptyList(self):
        url = '/clubs/'
        response = self.client.get(url, format='json')
        self.assertEqual(Club.objects.count(), len(response.data))

    def testListClubs_oneClubExistsInDb_returnsOneClubInResponse(self):
        url = '/clubs/'
        Club.objects.create(name="Bitbyte - The Programming Club",
                            category="S&T",
                            description="Aim to create thriving coding environment for developers.",
                            email="theprogclub@iiitdmj.ac.in <theprogclub@iiitdmj.ac.in>;",
                            logo="https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png")
        response = self.client.get(url, format='json')
        self.assertEqual(Club.objects.count(), len(response.data))
