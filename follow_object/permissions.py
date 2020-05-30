from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class MustBeLoggedIn(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        AnnonymousUsers are not allowed
        """
        return not isinstance(request.user, AnonymousUser)
