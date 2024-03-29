import uuid
from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.clubs.models import Club
from api.clubs.views import ClubRegistrationRequest
from api.roles.models import Role

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

        Role.objects.create(name='Coordinator',
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

    Role.objects.create(name=position,
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


@pytest.mark.django_db
@pytest.fixture(scope='function')
def test_club():
    return Club.objects.create(name='Bitbyte - The Programming Club',
                               category='S&T',
                               description='Some desc',
                               email='theprogclub@iiitdmj.ac.in',
                               logo='https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png')


@pytest.mark.django_db
@pytest.fixture(scope='function')
def test_user():
    return User.objects.create(email='test@user.com',
                               first_name='test',
                               last_name='User')


@pytest.mark.django_db
@pytest.fixture(scope='function')
def test_registration_request(test_user, test_club):
    return ClubRegistrationRequest.objects.create(user=test_user,
                                                  club=test_club,
                                                  fee_submitted=True,
                                                  status='Pending',
                                                  remark='Some text')


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.mark.django_db
def testCreateClubRegistrationRequest_ClubDoesNotExist_returnBadRequest(client, test_user):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.post('/clubs/19999/registration-requests/', {
        'fee_submitted': True,
        'status': 'Pending',
        'remark': 'Some text'
    })

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == 'invalid request'


@pytest.mark.django_db
def testCreateClubRegistrationRequest_validRequest_returnHTTP201(client, test_user, test_club):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.post(f'/clubs/{test_club.id}/registration-requests/', {
        'fee_submitted': True,
        'status': 'Pending',
        'remark': 'Some text'
    })

    # then

    # Removing updated_at at the time of testing ('updated_at' & datetime.now() )
    # can't be equal due to time delay  , time of updation and current time
    response.data.pop('updated_at', None)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'id': 1, 'user': test_user.id, 'club': test_club.id,
                             'fee_submitted': True, 'status': 'Pending', 'remark': 'Some text'}


@pytest.mark.django_db
def testUpdateClubRegistrationRequest_nonAdminRequest_throwsForbidden(client, test_user, test_club,
                                                                      test_registration_request):
    # given
    client.force_authenticate(test_user)

    # when
    url = f'/clubs/{test_club.id}/registration-requests/{test_registration_request.id}/'
    response = client.put(url, {
        'fee_submitted': True,
        'remark': 'Late fees',
        'status': 'Approved',
    })

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@ pytest.mark.django_db
def testUpdateClubRegistration_adminReq_invalidRequest_returnNotFound(client):
    # given
    user = User.objects.create(
        email='admin@user.com', first_name='admin', last_name='user', is_staff=True)
    client.force_authenticate(user)

    # when
    response = client.put('/clubs/999/registration-requests/99/', {
        'fee_submitted': True,
        'remark': 'Late fees',
        'status': 'Approved',
    })

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def testUpdateClubRegistrationRequest_adminRequestValidData_updated(client, test_club,
                                                                    test_registration_request):
    # given
    user = User.objects.create(
        email='admin@user.com', first_name='admin', last_name='user', is_staff=True)
    client.force_authenticate(user)

    # when
    url = f'/clubs/{test_club.id}/registration-requests/{test_registration_request.id}/'
    response = client.put(url, {
        'fee_submitted': True,
        'remark': 'Late fees',
        'status': 'Approved',
    })

    # then
    updated_registration_request = ClubRegistrationRequest.objects.get(
        pk=test_registration_request.id)

    # Only removing updated_at at the time of testing ('updated_at' & datetime.now() )
    # can't be equal due to time delay  , time of updation and current time
    response.data.pop('updated_at', None)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': test_registration_request.id,
                             'user': test_registration_request.user.id,
                             'club': test_registration_request.club.id,
                             'fee_submitted': True,
                             'remark': 'Late fees',
                             'status': 'Approved',
                             'updated_by': user.id}
    assert updated_registration_request.fee_submitted
    assert updated_registration_request.remark == 'Late fees'
    assert updated_registration_request.status == 'Approved'
    assert updated_registration_request.updated_by == user


@pytest.mark.django_db
@pytest.mark.parametrize('position', ['Coordinator', 'Co-Coordinator', 'Core member'])
def testUpdateClubRegistrationRequest_coreMemberRequestValidData_updated(client,
                                                                         position,
                                                                         test_club,
                                                                         test_registration_request):
    # given
    user = User.objects.create(
        email='core@user.com', first_name='core', last_name='member')
    client.force_authenticate(user)

    Role.objects.create(name=position,
                        club=test_club,
                        user=user,
                        assigned_at=date.today())

    # when
    url = f'/clubs/{test_club.id}/registration-requests/{test_registration_request.id}/'
    response = client.put(url, {
        'fee_submitted': True,
        'remark': 'Late fees',
        'status': 'Approved',
    })

    # then
    updated_registration_request = ClubRegistrationRequest.objects.get(
        pk=test_registration_request.id)

    # Only removing updated_at at the time of testing ('updated_at' & datetime.now()
    # can't be equal due to time delay  , time of updation and current time
    response.data.pop('updated_at', None)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': test_registration_request.id,
                             'user': test_registration_request.user.id,
                             'club': test_registration_request.club.id,
                             'fee_submitted': True,
                             'remark': 'Late fees',
                             'status': 'Approved',
                             'updated_by': user.id}
    assert updated_registration_request.fee_submitted
    assert updated_registration_request.remark == 'Late fees'
    assert updated_registration_request.status == 'Approved'
    assert updated_registration_request.updated_by == user
