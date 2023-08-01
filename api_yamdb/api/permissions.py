from rest_framework import permissions


class AdminPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.Role.ADMIN
