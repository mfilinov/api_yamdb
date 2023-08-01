from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        is_admin = bool(request.user.is_authenticated and
                        request.user.role == 'admin')
        is_superuser = bool(request.user and request.user.is_staff)
        return is_admin or is_superuser
