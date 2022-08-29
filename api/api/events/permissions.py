from django.db.models import Q
from rest_framework import permissions

from api.roles.models import Role


class IsCoreMemberOrAdminElseReadOnly(permissions.BasePermission):
    """ Permission to only allow core members, co-coordinators and coordiantors """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        allowed_roles = obj.club.roles.filter(
                        Q(name=Role.ROLE_CORE_MEMBER) |
                        Q(name=Role.ROLE_COORDINATOR) |
                        Q(name=Role.ROLE_CO_COORDINATOR))

        user_roles = request.user.roles.filter(club__id=obj.club.id)

        return (request.user.is_staff or (allowed_roles & user_roles).exists())
