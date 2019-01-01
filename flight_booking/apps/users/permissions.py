from rest_framework import permissions, exceptions

from .auth import VerifyToken


class PostPermission(permissions.BasePermission):
    """
    Custom permission to only authenticated user post a request.
    """

    def has_permission(self, request, view):
        # It only allow Post requests for authenticated users.
        if request.method == "POST":
            if VerifyToken().authenticate(request):
                return True
            return False
        return True


class GetAdminPermissions(permissions.BasePermission):
    """
    Custom permission to only allow Admin to fetch resource.
    """

    def has_permission(self, request, view):
        # It only allow GET requests for Admin.
        if request.method == "GET":
            authenticated_user, none_value = VerifyToken().authenticate(request)
            if authenticated_user is None or not authenticated_user.is_superuser:
                raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                      ' level to perform this action')
            return True
        return True


class GetAdminAndUserPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and Admin to fetch resource.
    """

    def has_permission(self, request, view):
        # It only allow GET requests for owners of an object and Admin.
        if request.method == "GET":
            authenticated_user, none_value = VerifyToken().authenticate(request)
            if authenticated_user.is_superuser:
                return True
            elif not authenticated_user or not str(authenticated_user.id) in request.path:
                raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                      ' level to perform this action')
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
        # It only allow GET requests for Admin.
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
            authenticated_user, none_value = VerifyToken().authenticate(request)
            if authenticated_user.is_superuser:
                return True
            elif not authenticated_user or not str(authenticated_user.id) in request.path:
                raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                      ' level to perform this action')
        return True


class PutAdminAndUserPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and Admin to update resource.
    """
    def has_permission(self, request, view):
        if request.method == "PUT":
            authenticated_user, none_value = VerifyToken().authenticate(request)
            if authenticated_user.is_superuser:
                return True
            elif not authenticated_user or not str(authenticated_user.id) in request.path:
                raise exceptions.AuthenticationFailed('Sorry, you do not have the permission'
                                                      ' level to perform this action')
        return True