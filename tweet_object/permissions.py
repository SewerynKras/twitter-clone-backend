from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class OnlyAuthorCanEdit(permissions.BasePermission):
    """
    Custom permission to only allow authors of a tweet to edit it.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the tweet.
        return obj.author == request.user.profile


class OnlyLoggedInUserCanViewList(permissions.BasePermission):
    """
    Custom permission to only allow users that are logged in to access the
    list view
    """

    def has_permission(self, request, view):
        if (
            view.action == 'list' and
            isinstance(request.user, AnonymousUser)
        ):
            return False

        return super().has_permission(request, view)
