from rest_framework import permissions

from profile_app.models import UserProfile


class IsCustomerUser(permissions.BasePermission):
    message = "Only customer accounts can create reviews."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.type == UserProfile.AccountType.CUSTOMER
        except UserProfile.DoesNotExist:
            return False


class IsReviewOwner(permissions.BasePermission):
    message = "Only the reviewer can update or delete this review."

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
