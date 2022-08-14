import pytest
from rest_framework import status
from rest_framework.test import APIClient

from api.clubs.models import Club
from api.events.models import Events
from api.roles.models import Roles


@pytest.mark.django_db
@pytest.fixture(scope='function')
def test_user(django_user_model):
    return django_user_model.objects.create(email='test@user.com',
                                            first_name='test',
                                            last_name='User')


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
def test_event(test_club):
    return Events.objects.create(name='Introduction to Git and Github',
                                 description='some desc',
                                 starts_at='2022-08-07',
                                 ends_at='2022-08-07',
                                 image_url='https://asite.com',
                                 address='c',
                                 club=test_club)


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.mark.django_db
def testRetrieveEvent_nonAdminAndNonCoreMemberRequest_throwsForbidden(
        client, test_user, test_event):
    # given
    client.force_authenticate(test_user)

    # response
    response = client.get(f'/events/{test_event.id}/', format='json')

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('position', [Roles.ROLE_COORDINATOR,
                                      Roles.ROLE_CO_COORDINATOR,
                                      Roles.ROLE_COORDINATOR])
def testRetrieveEvent_CoreMemberRequest_returnSuccesful(
        client, test_user, test_club, test_event, position):
    # given
    client.force_authenticate(test_user)
    Roles.objects.create(name=position,
                         club=test_club,
                         user=test_user,
                         assigned_at='2022-08-01')

    # when
    response = client.get(f'/events/{test_event.id}/', format='json')

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': test_event.id,
                             'name': 'Introduction to Git and Github',
                             'description': 'some desc',
                             'starts_at': '2022-08-07',
                             'ends_at': '2022-08-07',
                             'registration_required': False,
                             'created_by': None,
                             'image_url': 'https://asite.com',
                             'club': 1,
                             'registration_approval_required': False,
                             'address': 'c'}


@pytest.mark.django_db
def testRetrieveEvent_AdminRequest_returnSuccessful(client, test_user, test_event):
    # given
    client.force_authenticate(test_user)
    test_user.is_staff = True
    test_user.save()

    # when
    response = client.get(f'/events/{test_event.id}/', format='json')

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': test_event.id,
                             'name': 'Introduction to Git and Github',
                             'description': 'some desc',
                             'starts_at': '2022-08-07',
                             'ends_at': '2022-08-07',
                             'registration_required': False,
                             'created_by': None,
                             'image_url': 'https://asite.com',
                             'club': 1,
                             'registration_approval_required': False,
                             'address': 'c'}
