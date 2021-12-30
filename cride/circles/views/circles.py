"""Circles views."""

# Django REST Framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Memberships


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated)
    lookup_field = 'slug_name'

    # Filters backend
    filter_backend = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ('-members__count', '-rides_offered', '-rides_taken')
    filter_fields = ('verified', 'is_limited')

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Memberships.objects.create(
            user=user,
            profile=profile,
            is_admin=True,
            remaining_invitations=10
        )
