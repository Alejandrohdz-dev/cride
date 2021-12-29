"""Memberships permissions."""
# Django Rest Framework
from rest_framework.permissions import BasePermission

# Local
from cride.circles.models.memberships import Memberships

class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members.

    Expect that the views implementing this permission
    have a `circle` attribute assigned.
    """

    def has_permission(self, request, view):
        """Verify user is an active member of the circle."""
        try:
            Memberships.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Memberships.DoesNotExist:
            return False
        return True