from django.db.models import Q
from rest_framework import permissions


class IsPositionHolderOrAdmin(permissions.BasePermission):
    """Custom permission to allow only position holders of respective club and admins"""

    def has_object_permission(self, request, view, obj):
        allowed_roles = obj.roles.filter(Q(name='Coordinator') | Q(name='Co-Coordinator'))
        user_roles = request.user.roles.filter(club__id=obj.id)

        # return true when allowed_roles and users roles have common elements
        return (request.user.is_staff or (allowed_roles & user_roles).exists())
