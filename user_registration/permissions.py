from rest_framework import permissions


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a client
        return request.user.user_type == 'client'


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin
        return request.user.user_type == 'admin'


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an owner or an admin
        return request.user and (request.user.is_superuser or request.user.user_type == 'owner')
