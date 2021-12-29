"""Circle memberships views."""

# Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Local
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.circles.serializers.memberships import MembershipsModelSerializer
from cride.circles.models.circles import Circle
from cride.circles.models.memberships import Memberships

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Circle membership view set."""
    serializer_class = MembershipsModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [p() for p in permissions]

    def get_queryset(self):
        """Return circle members."""
        return Memberships.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        """Return the circle member by using the user's username."""
        return get_object_or_404(
            Memberships,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )

    def perform_destroy(self, instance):
        """Disable membership."""
        instance.is_active = False
        instance.save()