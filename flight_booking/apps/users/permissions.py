from rest_framework import permissions, exceptions

from .auth import VerifyToken
from .helpers import handle_admin_user_check


class GetAdminPermissions(permissions.BasePermission):
    """
    Custom permission to only allow Admin to fetch resource.
    """

    def has_permission(self, request, view):
        # It only allow GET requests for Admin.
        if request.method == "GET":
            IsAdmin().has_permission(request, view)
        return True


class GetAdminAndUserPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and Admin to fetch resource.
    """

    def has_permission(self, request, view):
        # It only allow GET requests for owners of an object and Admin.
        if request.method == "GET":
            return handle_admin_user_check(request)
        return True


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return str(request.user) in str(obj)


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow Admin to fetch resource.
    """

    def has_permission(self, request, view):
        authenticated_user, none_value = VerifyToken().authenticate(request)
        if authenticated_user.is_superuser:
            raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                  ' level to perform this action')
        return True


class PatchAdminAndUserPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and Admin to partially update resource.
    """
    def has_permission(self, request, view):
        if request.method == "PATCH":
            return handle_admin_user_check(request)
        return True


class PutAdminAndUserPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and Admin to update resource.
    """
    def has_permission(self, request, view):
        if request.method == "PUT":
            return handle_admin_user_check(request)
        return True
