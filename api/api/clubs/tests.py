import uuid
from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.clubs.models import Club
from api.roles.models import Roles

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
                                logo="https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png",
                                slug=uuid.uuid4())
        # when
        response = self.client.get('/clubs/', format='json')
        # then
        self.assertEqual(len(response.data['results']), 50)


class UpdateClubsViewTest(APITestCase):
    """Tests UpdateClubView for updating club details """

    @pytest.mark.django_db
    def testUpdateClubs_nonAdminRequest_throwsForbidden(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)

        test_club = Club.objects.create(name="Bitbyte - The Programming Club",
                                        category="S&T",
                                        description="Some desc here",
                                        email="theprogclub@iiitdmj.ac.in",
                                        logo="#")
        # when
        response = self.client.put(f'/clubs/{test_club.id}/', {'name': 'Bitbyte',
                                                               'category': "S&T",
                                                               'description': "Some desc here",
                                                               'email': "theprogclub@iiitdmj.ac.in",
                                                               'logo': "https://iiitdmj.ac.in"})

        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @pytest.mark.django_db
    def testUpdateClubs_adminRequest_updatesSuccessful(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User', is_staff=True)
        self.client.force_authenticate(user)

        test_club = Club.objects.create(name="Bitbyte - The Programming Club",
                                        category="S&T",
                                        description="Some desc here",
                                        email="theprogclub@iiitdmj.ac.in",
                                        logo="#",
                                        slug='tpc')

        # when
        response = self.client.put(f'/clubs/{test_club.id}/', {'name': 'changed_club_name',
                                                               'category': "S&T",
                                                               'description': "Some desc here",
                                                               'email': "theprogclub@iiitdmj.ac.in",
                                                               'logo': "https://iiitdmj.ac.in"})

        # then
        updated_club = Club.objects.get(pk=test_club.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1,
                                         'name': 'changed_club_name',
                                         'category': 'S&T',
                                         'logo': 'https://iiitdmj.ac.in',
                                         'description': 'Some desc here',
                                         'email': 'theprogclub@iiitdmj.ac.in',
                                         'slug': 'tpc'})
        self.assertEqual(updated_club.name, 'changed_club_name')
        self.assertEqual(updated_club.category, 'S&T')

    @pytest.mark.django_db
    def testUpdateClubs_incompleteInformationInRequest_throwsBadRequest(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)

        test_club = Club.objects.create(name="Bitbyte - The Programming Club",
                                        category="S&T",
                                        description="Some desc here",
                                        email="theprogclub@iiitdmj.ac.in",
                                        logo="#")

        Roles.objects.create(name='Coordinator',
                             club=test_club,
                             user=user,
                             assigned_at=date.today())

        # when
        # request is missing club email
        response = self.client.put(f'/clubs/{test_club.id}/', {'name': 'changed_club_name',
                                                               'category': "S&T",
                                                               'description': "Some desc here",
                                                               'logo': "https://iiitdmj.ac.in"})

        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
@pytest.mark.parametrize('position', ['Coordinator', 'Co-Coordinator'])
def testUpdateClubs_positionHolderRequest_updatesSuccessful(position):
    # given
    client = APIClient()
    user = User.objects.create(
        email='test@user.com', first_name='Test', last_name='User')
    client.force_authenticate(user)

    test_club = Club.objects.create(name="Bitbyte - The Programming Club",
                                    category="S&T",
                                    description="some_desc_here",
                                    email="theprogclub@iiitdmj.ac.in",
                                    logo="#",
                                    slug='tpc')

    Roles.objects.create(name=position,
                         club=test_club,
                         user=user,
                         assigned_at=date.today())
    # when
    response = client.put(f'/clubs/{test_club.id}/', {'name': 'changed_club_name',
                                                      'category': 'Cultural',
                                                      'description': 'some_desc_here',
                                                      'email': 'theprogclub@iiitdmj.ac.in',
                                                      'logo': 'https://changedlogo.com'
                                                      })

    # then
    updated_club = Club.objects.get(pk=test_club.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': 1,
                             'name': 'changed_club_name',
                             'category': 'Cultural',
                             'logo': 'https://changedlogo.com',
                             'description': 'some_desc_here',
                             'email': 'theprogclub@iiitdmj.ac.in',
                             'slug': 'tpc'}
    assert updated_club.name == 'changed_club_name'
    assert updated_club.category == 'Cultural'
    assert updated_club.logo == 'https://changedlogo.com'
    assert updated_club.email, 'theprogclub@iiitdmj.ac.in'
