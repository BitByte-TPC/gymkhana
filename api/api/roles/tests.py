from datetime import date
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from api.clubs.models import Club
from api.roles.models import Role

User = get_user_model()


@pytest.mark.django_db
def testCreateRole_nonAdminRequest_throwsForbidden():
    # given
    client = APIClient()
    test_user = User.objects.create(email='test@user.com',
                                    first_name='test',
                                    last_name='user')

    client.force_authenticate(test_user)

    test_club = Club.objects.create(name='Bitbyte - The Programming Club',
                                    category='S&T',
                                    description='Some desc',
                                    email='theprogclub@iiitdmj.ac.in',
                                    logo='https://asite.com',
                                    slug='tpc')

    # when
    response = client.post('/roles/', {'name': 'Coordinator',
                                       'club': test_club.id,
                                       'user': test_user.id,
                                       'active': True})

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('role', [Role.ROLE_COORDINATOR,
                                  Role.ROLE_CO_COORDINATOR,
                                  Role.ROLE_CORE_MEMBER,
                                  Role.ROLE_FACULTY_INCHARGE,
                                  Role.ROLE_CONVENER,
                                  Role.ROLE_CO_CONVENER,
                                  Role.ROLE_COUNSELLOR,
                                  Role.ROLE_ASSOCIATE_COUNSELLOR])
def testCreateRole_adminRequest_returnSuccesful(role):
    # given
    client = APIClient()
    test_user = User.objects.create(email='test@user.com',
                                    first_name='test',
                                    last_name='user',
                                    is_staff=True)

    test_club = Club.objects.create(name='Bitbyte - The Programming Club',
                                    category='S&T',
                                    description='Some desc',
                                    email='theprogclub@iiitdmj.ac.in',
                                    logo='https://asite.com',
                                    slug='tpc')

    client.force_authenticate(test_user)
    today = date.today().strftime("%Y-%m-%d")

    # when
    response = client.post('/roles/', {'name': role,
                                       'club': test_club.id,
                                       'user': test_user.id,
                                       'active': True})

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert Role.objects.count() == 1
    assert response.data == {'name': role,
                             'club': 1,
                             'user': 1,
                             'assigned_at': today,
                             'active': True}
