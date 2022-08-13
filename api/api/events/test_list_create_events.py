import pytest
from api.clubs.models import Club
from api.events.models import Events
from api.roles.models import Roles
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


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
                               logo='https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png',
                               slug='tpc')


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.mark.django_db
def testListEvent_noEventInDb_returnsEmptyList(test_user, client):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.get('/events/', format='json')

    # then
    assert response.data['count'] == 0


@pytest.mark.django_db
def testListEvent_oneEventInDb_returnsOneEventInResponse(client, test_user, test_club):
    # given
    client.force_authenticate(test_user)

    Events.objects.create(name='Introduction to Git and Github',
                          description='some desc',
                          starts_at='2022-08-07',
                          ends_at='2022-08-07',
                          image_url='https://asite.com',
                          address='c',
                          club=test_club)

    # when
    response = client.get('/events/', format='json')

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


@pytest.mark.django_db
@pytest.mark.parametrize('position', [Roles.ROLE_CORE_MEMBER,
                                      Roles.ROLE_CO_COORDINATOR,
                                      Roles.ROLE_COORDINATOR])
def testCreateEvent_coreMemberRequest_creationSuccessful(client, test_user, test_club, position):
    # given
    client.force_authenticate(test_user)
    Roles.objects.create(name=position,
                         club=test_club,
                         user=test_user,
                         assigned_at='2022-08-01')

    # when
    response = client.post('/events/', {'name': 'Introduction to Git and Github',
                                        'description': 'some desc',
                                        'starts_at': '2022-08-07',
                                        'ends_at': '2022-08-07',
                                        'image_url': 'https://asite.com',
                                        'address': 'c',
                                        'club': test_club.id
                                        })

    # then
    created_event = Events.objects.get(id=response.data['id'])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'id': created_event.id,
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
    assert created_event.name == 'Introduction to Git and Github'


@pytest.mark.django_db
def testCreateEvent_adminRequest_creationSuccessful(client, test_user, test_club):
    # given
    test_user.is_staff = True
    test_user.save()
    client.force_authenticate(test_user)

    # when
    response = client.post('/events/', {'name': 'Introduction to Git and Github',
                                        'description': 'some desc',
                                        'starts_at': '2022-08-07',
                                        'ends_at': '2022-08-07',
                                        'image_url': 'https://asite.com',
                                        'address': 'c',
                                        'club': test_club.id
                                        })

    # then
    created_event = Events.objects.get(id=response.data['id'])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'id': created_event.id,
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
    assert created_event.name == 'Introduction to Git and Github'


@pytest.mark.django_db
def testCreateEvent_unauthorizedUserRequest_throwsForbidden(client, test_user, test_club):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.post('/events/', {'name': 'Introduction to Git and Github',
                                        'description': 'some desc',
                                        'starts_at': '2022-08-07',
                                        'ends_at': '2022-08-07',
                                        'image_url': 'https://asite.com',
                                        'address': 'c',
                                        'club': test_club.id
                                        })
    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def testCreateEvent_missingDataInRequest_throwsBadRequest(client, test_user, test_club):
    # given
    client.force_authenticate(test_user)

    # when
    # request missing start and end time
    response = client.post('/events/', {'name': 'Introduction to Git and Github',
                                        'description': 'some desc',
                                        'image_url': 'https://asite.com',
                                        'address': 'c',
                                        'club': test_club.id
                                        })

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
                            'starts_at': [
                                'This field is required.'
                            ],
                            'ends_at': [
                                'This field is required.'
                            ]
                           }
