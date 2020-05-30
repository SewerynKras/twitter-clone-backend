from rest_framework import permissions


class CanOnlyEditYourself(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profiles.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the user.
        return obj == request.user
