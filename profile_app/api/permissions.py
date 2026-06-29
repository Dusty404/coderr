from rest_framework import permissions


class IsOwnProfileOrReadOnly(permissions.BasePermission):
    """
    Allows read access to profiles and restricts writes to the owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.user == request.user
