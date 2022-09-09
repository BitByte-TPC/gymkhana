from django.db.models import Q
from rest_framework import permissions

from api.roles.models import Role


class IsPositionHolderOrAdmin(permissions.BasePermission):
    """Custom permission to allow only position holders of respective club and admins"""

    def has_object_permission(self, request, view, obj):
        allowed_roles = obj.roles.filter(Q(name=Role.ROLE_COORDINATOR) | Q(
            name=Role.ROLE_CO_COORDINATOR) | Q(name=Role.ROLE_CORE_MEMBER))
        user_roles = request.user.roles.filter(club__id=obj.id)

        # return true when allowed_roles and users roles have common elements
        return (request.user.is_staff or (allowed_roles & user_roles).exists())


class IsCoreMemberOrAdmin(permissions.BasePermission):
    """Custom permission to allow only core members of respective club and admins"""

    def has_permission(self, request, view):
        user_roles = request.user.roles.filter(Q(name=Role.ROLE_COORDINATOR) | Q(
            name=Role.ROLE_CO_COORDINATOR) | Q(name=Role.ROLE_CORE_MEMBER))

        # return true when allowed_roles and users roles have common elements
        return (request.user.is_staff or user_roles.exists())

    def has_object_permission(self, request, view, obj):
        allowed_roles = obj.club.roles.filter(Q(name=Role.ROLE_COORDINATOR) | Q(
            name=Role.ROLE_CO_COORDINATOR) | Q(name=Role.ROLE_CORE_MEMBER))
        user_roles = request.user.roles.filter(club__id=obj.club.id)

        # return true when allowed_roles and users roles have common elements
        return (request.user.is_staff or (allowed_roles & user_roles).exists())
