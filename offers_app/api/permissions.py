from rest_framework import permissions

from profile_app.models import UserProfile


class IsBusinessUser(permissions.BasePermission):
    """
    Allows offer creation only for users with a business profile.
    """
    message = "Nur Business-Accounts können Angebote erstellen."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.type == UserProfile.AccountType.BUSINESS
        except UserProfile.DoesNotExist:
            return False


class IsOfferOwner(permissions.BasePermission):
    """
    Allows offer changes only for the user who created the offer.
    """
    message = "Nur der Ersteller des Angebotes darf dieses bearbeiten oder löschen."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
