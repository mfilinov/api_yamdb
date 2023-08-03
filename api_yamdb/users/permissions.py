from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        is_admin = bool(request.user.is_authenticated and
                        request.user.role == User.Role.ADMIN)
        is_superuser = bool(request.user.is_staff)
        return is_admin or is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsModeratorUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.role == User.Role.MODERATOR)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        is_owner = bool(request.user.is_authenticated and
                        obj.author == request.user)
        return is_owner
