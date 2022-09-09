from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from api.clubs.models import Club
from api.roles.models import Role

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
                               slug='slug field')


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.mark.django_db
def testListRoles_userHasNoRoles_returnsEmptyList(client, test_user):
    # given
    client.force_authenticate(test_user)

    # when
    response = client.get('/users/accounts/me/roles/', format='json')

    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def testListRoles_userHasHundredRoles_returnsFirstFiftyRolesList(client, test_user, test_club):
    # given
    client.force_authenticate(test_user)

    for i in range(0, 100):
        Role.objects.create(name='Coordinator', user=test_user, club=test_club,
                            assigned_at=date.today(), active=True)

    # when
    response = client.get('/users/accounts/me/roles/', format='json')

    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 50
