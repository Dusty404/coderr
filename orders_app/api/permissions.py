from rest_framework import permissions

from profile_app.models import UserProfile


class IsCustomerUser(permissions.BasePermission):
    """
    Allows order creation only for users with a customer profile.
    """
    message = "Only customer accounts can create orders."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.type == UserProfile.AccountType.CUSTOMER
        except UserProfile.DoesNotExist:
            return False


class IsBusinessUser(permissions.BasePermission):
    """
    Allows order updates only for users with a business profile.
    """
    message = "Only business accounts can update orders."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.type == UserProfile.AccountType.BUSINESS
        except UserProfile.DoesNotExist:
            return False
