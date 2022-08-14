from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from api.clubs.models import Club
from api.roles.models import Roles

User = get_user_model()


class ListUserRolesTest(APITestCase):
    """Tests ListRolesView for getting the list of clubs where user is a core member."""
    @pytest.mark.django_db
    def testListRoles_userIsNot_CoreMember_returnsHTTPNotFound(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User', is_staff=True)
        self.client.force_authenticate(user)

        club = Club.objects.create(name="Bitbyte - The Programming Club",
                                        category="S&T",
                                        description="Some desc here",
                                        email="theprogclub@iiitdmj.ac.in",
                                        logo="https://iiitdmj.ac.in")
        Roles.objects.create(name='Faculty Incharge', user=user,
                             club=club, assigned_at=date.today(), active=True)

        # when

        response = self.client.get(f'/users/{user.id}/roles/')
        # then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testListRoles_userIs_CoreMember_returnsRolesList(self):
        # given
        user = User.objects.create(
            email='test@user.com', first_name='Test', last_name='User', is_staff=True)
        self.client.force_authenticate(user)

        club = Club.objects.create(name="Bitbyte - The Programming Club",
                                        category="S&T",
                                        description="Some desc here",
                                        email="theprogclub@iiitdmj.ac.in",
                                        logo="https://iiitdmj.ac.in")
        Roles.objects.create(name='Coordinator', user=user, club=club,
                             assigned_at=date.today(), active=True)
        Roles.objects.create(name='Co-Coordinator', user=user, club=club,
                             assigned_at=date.today(), active=True)
        Roles.objects.create(name='Core member', user=user, club=club,
                             assigned_at=date.today(), active=True)
        # when
        response = self.client.get(f'/users/{user.id}/roles/')
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
