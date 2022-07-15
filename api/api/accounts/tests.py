import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()
userCreationEndpoint = '/users/'
primaryTestUserMail = 'test@user.com'


class UsersListViewTest(APITestCase):

    @pytest.mark.django_db
    def testUsersListView_testBaseUserModel_validEmailProvided_userSuccessfullyCreated(self):
        # given
        user = User.objects.create(
            email=primaryTestUserMail, first_name='Test', last_name='User')
        self.client.force_authenticate(user)
        testUserEmail = 'test1@user.com'

        # when
        response = self.client.post(userCreationEndpoint, {'email': testUserEmail}, format='json')

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], testUserEmail)

    @pytest.mark.django_db
    def testUsersListView_invalidEmailsProvided_returnsHttp400(self):
        # given
        user = User.objects.create(
            email=primaryTestUserMail, first_name='Test', last_name='User')
        self.client.force_authenticate(user)

        invalidTestMail1 = primaryTestUserMail
        invalidTestMail2 = ''
        invalidTestMail3 = 'testusercom'

        # when
        response1 = self.client.post(userCreationEndpoint, {'email': invalidTestMail1},
                                     format='json')
        response2 = self.client.post(userCreationEndpoint, {'email': invalidTestMail2},
                                     format='json')
        response3 = self.client.post(userCreationEndpoint, {'email': invalidTestMail3},
                                     format='json')

        # then
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def testUsersListView_testStudentModel_validDataProvided_userSuccessfullyCreated(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)

        testUserEmail = 'test@student.com'

        # when
        response = self.client.post(userCreationEndpoint,
                                    {
                                      'email': testUserEmail,
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], testUserEmail)
        self.assertEqual(response.data['student']['roll_no'], '21abc000')

    @pytest.mark.django_db
    def testUserListView_testFacultyModel_validDataProvided_userSuccessfullyCreated(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)

        testUserEmail = 'test@faculty.com'

        # when
        response = self.client.post(userCreationEndpoint,
                                    {
                                      'email': testUserEmail,
                                      'gender': 'F',
                                      'user_type': 'Faculty',
                                      'faculty': {
                                          'title': 'Prof',
                                          'department': 'ECE',
                                          'designation': 'z'
                                      }
                                    })

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], testUserEmail)
        self.assertEqual(response.data['faculty']['title'], 'Prof')

    @pytest.mark.django_db
    def testUserListView_testStaffModel_validDataProvided_userSuccessfullyCreated(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User')
        self.client.force_authenticate(user)

        testUserEmail = 'test@staff.com'

        # when
        response = self.client.post(userCreationEndpoint,
                                    {
                                      'email': testUserEmail,
                                      'gender': 'M',
                                      'last_name': 'Staff',
                                      'user_type': 'Staff',
                                      'staff': {
                                          'department': 'ECE',
                                          'designation': 'z'
                                      }
                                    })

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], testUserEmail)
        self.assertEqual(response.data['staff']['department'], 'ECE')
