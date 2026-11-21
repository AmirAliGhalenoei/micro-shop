from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    """
        Allow access only to users who are not logged in.
    """
    message = "You are already logged in."

    def has_permission(self, request, view):
        return not request.user.is_authenticated