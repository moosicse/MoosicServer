from rest_framework import permissions


class AllowAllPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class LoginRequired(permissions.BasePermission):
    message = 'You do not have permission to access this one.'

    def has_permission(self, request, view):
        user = request.user
        if user is None:
            return False
        return True


class AccountPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        # if user.is_superuser or user.is_staff:
        #     return True
        return user == obj.user


class StaffRequired(permissions.BasePermission):
    message = 'You do not have permission to access this one.'

    def has_permission(self, request, view):
        user = request.user
        if user is None:
            return False

        if user.is_superuser or user.is_staff:
            return True

        return False
