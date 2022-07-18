from collections import OrderedDict

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import Faculty, Staff, Student

User = get_user_model()
primary_test_user_mail = 'test@user.com'


@pytest.mark.django_db
@pytest.fixture(scope='function')
def test_user(django_user_model):
    return django_user_model.objects.create(email=primary_test_user_mail,
                                            first_name='test',
                                            last_name='user')


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.mark.django_db
def testUpdateUserView_nonOwnerAndNonAdminRequest_throwsForbidden(client, test_user):

    # given
    client.force_authenticate(test_user)
    new_user = User.objects.create(email='new@user.com',
                                   first_name='new',
                                   last_name='user')

    # when
    response = client.put(f'/users/{new_user.id}/', {'email': 'changed_mail@user.com'})

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def testUpdateUserView_baseUserInRequest_ownerChangeRequest_updatesSuccessful(client, test_user):

    # given
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'last_name': 'changed_name'})

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['last_name'] == 'changed_name'
    assert updated_test_user.last_name == 'changed_name'


@pytest.mark.django_db
def testUpdateUserView_baseUserInRequest_adminChangeRequest_updatesSuccessful(client, test_user):

    # given
    admin_user = User.objects.create(email='admin@user.com',
                                     first_name='admin',
                                     is_staff=True)

    client.force_authenticate(admin_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'email': 'test@user.com',
                                                      'first_name': 'changed_name'})

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'changed_name'
    assert updated_test_user.first_name == 'changed_name'


@pytest.mark.django_db
def testUpdateUserView_baseUserInRequest_addStudentInformation_updatesSuccessful(client, test_user):

    # given
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'student': {
                                                          'roll_no': '21abc000',
                                                          'batch': 2025,
                                                          'department': 'CSE',
                                                          'hostel_address': 'H3-Z000'
                                                          }
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'email': 'test@user.com',
                             'first_name': 'test',
                             'last_name': 'user',
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Student',
                             'picture_url': '',
                             'student': OrderedDict([('roll_no', '21abc000'),
                                                     ('batch', 2025),
                                                     ('department', 'CSE'),
                                                     ('hostel_address', 'H3-Z000'),
                                                     ('bio', None)]),
                             'faculty': None,
                             'staff': None
                             }

    assert updated_test_user.student.roll_no == '21abc000'


@pytest.mark.django_db
def testUpdateUserView_baseUserInResquest_addFacultyInformation_updatesSuccessful(
      client,
      test_user):

    # given
    test_user.user_type = 'Faculty'
    test_user.save()
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'user_type': 'Faculty',
                                                      'faculty': {
                                                          'title': 'Prof',
                                                          'department': 'CSE',
                                                          'designation': 'smthng'
                                                          }
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'email': 'test@user.com',
                             'first_name': 'test',
                             'last_name': 'user',
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Faculty',
                             'picture_url': '',
                             'student': None,
                             'faculty': OrderedDict([('title', 'Prof'),
                                                     ('department', 'CSE'),
                                                     ('designation', 'smthng')]),
                             'staff': None
                             }

    assert updated_test_user.faculty.title == 'Prof'


@pytest.mark.django_db
def testUpdateUserView_baseUserInRequest_addStaffInformation_updatesSuccessful(client, test_user):

    # given
    test_user.user_type = 'Staff'
    test_user.save()
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'user_type': 'Staff',
                                                      'staff': {
                                                          'department': 'ECE',
                                                          'designation': 'smthng'
                                                          }
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'email': 'test@user.com',
                             'first_name': 'test',
                             'last_name': 'user',
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Staff',
                             'picture_url': '',
                             'student': None,
                             'faculty': None,
                             'staff': OrderedDict([('department', 'ECE'),
                                                   ('designation', 'smthng')])
                             }

    assert updated_test_user.staff.department == 'ECE'


@pytest.mark.django_db
def testUpdateUserView_studentUserInRequest_changeRequest_updatesSuccessful(client, test_user):

    # given
    Student.objects.create(user=test_user,
                           roll_no='21abc000',
                           batch=2025,
                           department='CSE',
                           bio='zzz')
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'student': {
                                                          'roll_no': '21abc000',
                                                          'batch': 2025,
                                                          'department': 'CSE',
                                                          'hostel_address': 'H3 Z111'}
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'email': 'test@user.com',
                             'first_name': 'test',
                             'last_name': 'user',
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Student',
                             'picture_url': '',
                             'student': OrderedDict([('roll_no', '21abc000'),
                                                     ('batch', 2025),
                                                     ('department', 'CSE'),
                                                     ('hostel_address', 'H3 Z111'),
                                                     ('bio', 'zzz')]),
                             'faculty': None,
                             'staff': None}

    assert updated_test_user.student.hostel_address == 'H3 Z111'


@pytest.mark.django_db
def testUpdateUserView_facultyUserInRequest_changeRequest_updatesSuccessful(client, test_user):

    # given
    test_user.user_type = "Faculty"
    test_user.save()
    Faculty.objects.create(user=test_user,
                           title='Prof',
                           department='CSE',
                           designation='smthng')
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'gender': 'F',
                                                      'faculty': {
                                                          'title': 'Prof',
                                                          'department': 'CSE',
                                                          'designation': 'smthng_different'}
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'email': 'test@user.com',
                             'first_name': 'test',
                             'last_name': 'user',
                             'gender': 'F',
                             'contact_no': None,
                             'user_type': 'Faculty',
                             'picture_url': '',
                             'student': None,
                             'faculty': OrderedDict([('title', 'Prof'),
                                                     ('department', 'CSE'),
                                                     ('designation', 'smthng_different')]),
                             'staff': None}

    assert updated_test_user.faculty.designation == 'smthng_different'
    assert updated_test_user.gender == 'F'


@pytest.mark.django_db
def testUpdateUserView_staffUserInRequest_changeRequest_updatesSuccessful(client, test_user):

    # given
    setattr(test_user, 'user_type', 'Staff')
    test_user.save()
    Staff.objects.create(user=test_user,
                         department='SM',
                         designation='smthng')
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'email': 'test@user.com',
                                                      'user_type': 'Staff',
                                                      'staff': {
                                                          'department': 'SM',
                                                          'designation': 'smthng_different'}
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'email': 'test@user.com',
                             'first_name': 'test',
                             'last_name': 'user',
                             'gender': 'M',
                             'contact_no': None,
                             'user_type': 'Staff',
                             'picture_url': '',
                             'student': None,
                             'faculty': None,
                             'staff': OrderedDict([('department', 'SM'),
                                                   ('designation', 'smthng_different')])
                             }

    assert updated_test_user.staff.designation == 'smthng_different'


@pytest.mark.django_db
@pytest.mark.parametrize('non_editable_field, value', [
                         ('email', 'changed@mail.com'),
                         ('user_type', 'Staff'),
                         ])
def testUpdateUserView_baseUserInRequest_ownerChangeRequestOfNonEditableField_nonEditableChangesIgnored(    # noqa: E501
      client,
      test_user,
      non_editable_field,
      value):

    # given
    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {non_editable_field: value})
    updated_test_user = User.objects.get(id=test_user.id)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data[non_editable_field] == getattr(test_user, non_editable_field)
    assert getattr(test_user, non_editable_field) == getattr(updated_test_user, non_editable_field)


@pytest.mark.django_db
@pytest.mark.parametrize('non_editable_field, value', [
                         ('email', 'changed@mail.com'),
                         ('user_type', 'Staff'),
                         ])
def testUpdateUserView_baseUserInRequest_adminChangeRequestOfNonEditableField_changesSuccesful(
      client,
      test_user,
      non_editable_field,
      value):

    # given
    admin_user = User.objects.create(email='admin@user.com', is_staff=True)
    client.force_authenticate(admin_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {non_editable_field: value})

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[non_editable_field] == value
    assert getattr(updated_test_user, non_editable_field) == value


@pytest.mark.django_db
@pytest.mark.parametrize('non_editable_field, value', [
                         ('roll_no', 'changed_roll_no'),
                         ('batch', 2024),
                         ('department', 'ME')
                         ])
def testUpdateUserView_studentUserInRequest_ownerChangeRequestOfNonEditableField_nonEditableChangeIgnored(    # noqa: E501
      client,
      test_user,
      non_editable_field,
      value):

    # given
    Student.objects.create(user=test_user,
                           roll_no='21abc000',
                           batch=2025,
                           department='CSE',
                           bio='zzz')
    test_user.user_type = 'Student'
    test_user.save()

    client.force_authenticate(test_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {non_editable_field: value})
    updated_test_user = User.objects.get(id=test_user.id)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data['student'][non_editable_field] == getattr(test_user.student,
                                                                   non_editable_field)
    assert getattr(test_user.student, non_editable_field) == getattr(updated_test_user.student,
                                                                     non_editable_field)


@pytest.mark.django_db
def testUpdateUserView_studentUserInRequest_adminChangeRequestOfNonEditableField_changesSuccesful(
      client,
      test_user):

    # given
    admin_user = User.objects.create(email='admin@user.com', is_staff=True)

    Student.objects.create(user=test_user,
                           roll_no='21abc000',
                           batch=2025,
                           department='CSE',
                           bio='zzz')

    test_user.user_type = 'Student'
    test_user.save()

    client.force_authenticate(admin_user)

    # when
    response = client.put(f'/users/{test_user.id}/', {'student': {
                                                          'roll_no': 'changed_roll_no',
                                                          'batch': 2025,
                                                          'department': 'CSE',
                                                          'hostel_address': 'changed_hostel_address'
                                                          }
                                                      })

    # then
    updated_test_user = User.objects.get(id=test_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['student']['roll_no'] == 'changed_roll_no'
    assert getattr(updated_test_user.student, 'roll_no') == 'changed_roll_no'
    assert getattr(updated_test_user.student, 'hostel_address') == 'changed_hostel_address'


@pytest.mark.django_db
def testUpdateUserView_studentUserInRequest_staffDataProvided_ignoresStaffDataChanges(
      client,
      test_user):

    # given
    Student.objects.create(user=test_user,
                           roll_no='21abc000',
                           batch=2025,
                           department='CSE',
                           bio='zzz')
    test_user.user_type = 'Student'
    test_user.save()

    client.force_authenticate(test_user)

    # when
    updated_test_user = User.objects.get(id=test_user.id)
    response = client.put(f'/users/{test_user.id}/', {'staff': {
                                                          'department': 'CSE',
                                                          'designation': 'smthng'
                                                          }
                                                      })

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data['student']['roll_no'] == '21abc000'
    assert updated_test_user.student.roll_no == '21abc000'
