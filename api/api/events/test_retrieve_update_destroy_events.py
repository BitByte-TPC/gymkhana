import pytest
from rest_framework import status
from rest_framework.test import APIClient

from api.clubs.models import Club
from api.events.models import Events
from api.roles.models import Role


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
def testRetrieveEvent_nonAdminAndNonCoreMemberRequest_returnSuccessful(
        client, test_user, test_event):
    # given
    client.force_authenticate(test_user)

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
@pytest.mark.parametrize('position', [Role.ROLE_CORE_MEMBER,
                                      Role.ROLE_CO_COORDINATOR,
                                      Role.ROLE_COORDINATOR])
def testRetrieveEvent_CoreMemberRequest_returnSuccesful(
        client, test_user, test_club, test_event, position):
    # given
    client.force_authenticate(test_user)
    Role.objects.create(name=position,
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


@pytest.mark.django_db
def testUpdateEvent_nonAdminAndNonCoreMemberRequest_throwsForbidden(
        client, test_user, test_club, test_event):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/events/{test_event.id}/', {'name': 'Introduction to Git',
                                                        'description': 'some other desc',
                                                        'starts_at': '2022-08-07',
                                                        'ends_at': '2022-08-07',
                                                        'image_url': 'https://asite.com',
                                                        'club': test_club.id,
                                                        'address': 'c'})

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('position', [Role.ROLE_CORE_MEMBER,
                                      Role.ROLE_CO_COORDINATOR,
                                      Role.ROLE_COORDINATOR])
def testUpdateEvent_coreMemberRequest_returnSuccesful(
        client, test_user, test_club, test_event, position):
    # given
    client.force_authenticate(test_user)
    Role.objects.create(name=position,
                        club=test_club,
                        user=test_user,
                        assigned_at='2022-08-01')

    # when
    response = client.put(f'/events/{test_event.id}/', {'name': 'Introduction to Git',
                                                        'description': 'some other desc',
                                                        'starts_at': '2022-08-07',
                                                        'ends_at': '2022-08-07',
                                                        'image_url': 'https://asite.com',
                                                        'club': test_club.id,
                                                        'address': 'c'})

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': test_event.id,
                             'name': 'Introduction to Git',
                             'description': 'some other desc',
                             'starts_at': '2022-08-07',
                             'ends_at': '2022-08-07',
                             'registration_required': False,
                             'created_by': None,
                             'image_url': 'https://asite.com',
                             'club': 1,
                             'registration_approval_required': False,
                             'address': 'c'}


def testUpdateEvent_adminRequest_returnSuccesful(
        client, test_user, test_club, test_event):
    # given
    client.force_authenticate(test_user)
    test_user.is_staff = True
    test_user.save()

    # when
    response = client.put(f'/events/{test_event.id}/', {'name': 'Introduction to Git',
                                                        'description': 'some other desc',
                                                        'starts_at': '2022-08-07',
                                                        'ends_at': '2022-08-07',
                                                        'image_url': 'https://asite.com',
                                                        'club': test_club.id,
                                                        'address': 'c'})

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'id': test_event.id,
                             'name': 'Introduction to Git',
                             'description': 'some other desc',
                             'starts_at': '2022-08-07',
                             'ends_at': '2022-08-07',
                             'registration_required': False,
                             'created_by': None,
                             'image_url': 'https://asite.com',
                             'club': 1,
                             'registration_approval_required': False,
                             'address': 'c'}


@pytest.mark.django_db
def testDestroyEvent_nonCoreMemberAndNonAdminRequest_throwsForbidden(
        client, test_user, test_club, test_event):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.delete(f'/events/{test_event.id}/')

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('position', [Role.ROLE_CORE_MEMBER,
                                      Role.ROLE_CO_COORDINATOR,
                                      Role.ROLE_COORDINATOR])
def testDestroyEvent_coreMemberRequest_returnSuccessful(
        client, test_user, test_club, test_event, position):
    # given
    client.force_authenticate(test_user)
    Role.objects.create(name=position,
                        club=test_club,
                        user=test_user,
                        assigned_at='2022-08-01')

    # when
    response = client.delete(f'/events/{test_event.id}/')

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Events.objects.count() == 0


@pytest.mark.django_db
def testDestroyEvent_adminRequest_returnSuccessful(
        client, test_user, test_club, test_event):
    # given
    client.force_authenticate(test_user)
    test_user.is_staff = True
    test_user.save()

    # when
    response = client.delete(f'/events/{test_event.id}/')

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Events.objects.count() == 0
