from rest_framework import permissions


class IsUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj == request.user


class IsHostOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not hasattr(obj, 'host'):
            return False

        if request.user.is_staff:
            return True

        return obj.host == request.user
