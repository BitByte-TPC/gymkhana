from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Custom permission to allow only Owners of profile and Admin Users"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj or request.user.is_staff
