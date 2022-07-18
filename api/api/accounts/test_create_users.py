from collections import OrderedDict

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()
user_creation_endpoint = '/users/'
primary_test_user_mail = 'test@user.com'


@pytest.mark.django_db
@pytest.fixture(scope='function')
def admin_user(django_user_model):
    return django_user_model.objects.create(email=primary_test_user_mail,
                                            first_name='test',
                                            last_name='User',
                                            is_staff=True)


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.mark.django_db
def testCreateUserView_testPermission_nonAdminRequest_throwsForbidden(client):
    # given
    user = User.objects.create(
        email=primary_test_user_mail, first_name='Test', last_name='User')
    client.force_authenticate(user)
    test_user_email = 'test1@user.com'

    # when
    response = client.post(user_creation_endpoint, {'email': test_user_email},
                           format='json')

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def testCreateUserView_testBaseUserModel_validEmailProvided_userSuccessfullyCreated(
      admin_user,
      client):

    # given
    client.force_authenticate(admin_user)
    test_user_email = 'test1@user.com'

    # when
    response = client.post(user_creation_endpoint,
                           {'email': test_user_email}, format='json')

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'email': 'test1@user.com',
                             'first_name': None,
                             'last_name': None,
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Student',
                             'picture_url': '',
                             'student': None,
                             'faculty': None,
                             'staff': None
                             }


@pytest.mark.django_db
@pytest.mark.parametrize('invalid_mail', [
    'test@user.com',  # admin user
    '',  # empty email
    'testusersom'  # invalid email format
])
def testCreateUserView_invalidEmailProvided_throwsBadRequest(admin_user, client, invalid_mail):
    # given
    client.force_authenticate(admin_user)

    # when
    response = client.post(user_creation_endpoint, {'email': invalid_mail},
                           format='json')

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def testCreateUserView_testStudentModel_validDataProvided_userCreatedSuccessfully(
      admin_user,
      client):
    # given
    client.force_authenticate(admin_user)

    test_user_email = 'test@student.com'

    # when
    response = client.post(user_creation_endpoint,
                           {'email': test_user_email,
                            'first_name': "test",
                            'user_type': 'Student',
                            'student': {
                                'roll_no': "21abc000",
                                'batch': 2025,
                                'department': "CSE",
                                'hostel_address': "H3-Z000"
                                }
                            })

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == test_user_email
    assert response.data['student']['roll_no'] == '21abc000'


@pytest.mark.django_db
def testCreateUserView_testFacultyModel_validDataProvided_userCreatedSuccessfully(
      admin_user,
      client):
    # given
    client.force_authenticate(admin_user)

    test_user_email = 'test@faculty.com'

    # when
    response = client.post(user_creation_endpoint,
                           {'email': test_user_email,
                            'gender': 'F',
                            'user_type': 'Faculty',
                            'faculty': {
                                'title': 'Prof',
                                'department': 'ECE',
                                'designation': 'z'
                                }
                            })

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == test_user_email
    assert response.data['faculty']['title'] == 'Prof'


@pytest.mark.django_db
def testCreateUserView_testStaffModel_validDataProvided_userCreatedSuccessfully(
      admin_user,
      client):
    # given
    client.force_authenticate(admin_user)

    test_user_email = 'test@staff.com'

    # when
    response = client.post(user_creation_endpoint,
                           {'email': test_user_email,
                            'gender': 'M',
                            'last_name': 'Staff',
                            'user_type': 'Staff',
                            'staff': {
                                'department': 'ECE',
                                'designation': 'z'
                                }
                            })

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'email': 'test@staff.com',
                             'first_name': None,
                             'last_name': 'Staff',
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Staff',
                             'picture_url': '',
                             'student': None,
                             'faculty': None,
                             'staff': OrderedDict([('department', 'ECE'),
                                                   ('designation', 'z')])
                             }


@pytest.mark.django_db
def testCreateUserView_usertypeAndProvidedDataMismatch_mismatchIsHandledAndUserCreatedSuccesfully(
      admin_user,
      client):

    # given
    client.force_authenticate(admin_user)

    # when
    response = client.post(user_creation_endpoint,
                           {'email': 'test@staff.com',
                            'user_type': 'Faculty',
                            'faculty': {
                                'title': 'Prof',
                                'department': 'ME'
                            },
                            'staff': {
                                'department': 'ECE',
                                'designation': 'z'
                                }
                            })

    # then
    created_user = User.objects.get(email='test@staff.com')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'email': 'test@staff.com',
                             'first_name': None,
                             'last_name': None,
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Faculty',
                             'picture_url': '',
                             'student': None,
                             'faculty': OrderedDict([('title', 'Prof'),
                                                     ('department', 'ME'),
                                                     ('designation', None)]),
                             'staff': None
                             }

    assert created_user.email == 'test@staff.com'
    assert created_user.faculty.title == 'Prof'
