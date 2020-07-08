from rest_framework import permissions


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
