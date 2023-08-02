from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        is_admin = bool(request.user.is_authenticated
                        and request.user.role == 'admin')
        is_superuser = bool(request.user and request.user.is_staff)
        return is_admin or is_superuser


class IsAuthorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_author = bool(request.user.is_authenticated
                         and request.user.id == obj.author.id)
        is_moderator = bool(request.user.is_authenticated
                            and request.user.role == 'moderator')
        is_admin = bool(request.user.is_authenticated
                        and request.user.role == 'admin')
        is_superuser = bool(request.user and request.user.is_staff)
        return is_author or is_moderator or is_admin or is_superuser
