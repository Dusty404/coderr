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

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.type == UserProfile.AccountType.BUSINESS
        except UserProfile.DoesNotExist:
            return False
        

class IsOrderRelatedBusiness(permissions.BasePermission):
    """
    Allows order updates only for the busniss related to the order.
    """
    message = "Only the order related business account can update this orders."

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.id == obj.business_user_id:
            return True
        return False


class IsAdminUserObjectPermission(permissions.BasePermission):
    """
    Allows access only to admin users after the target object was resolved.
    """
    message = "Only admin users can delete orders."

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)
