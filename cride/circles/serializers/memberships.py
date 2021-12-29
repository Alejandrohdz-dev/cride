"""Memberships serializer."""

# Django Rest Framework
from rest_framework import serializers

# Local
from cride.users.serializers.users import UserModelSerializer
from cride.circles.models import Memberships


class MembershipsModelSerializer(serializers.ModelSerializer):
    """Memberships model serializer."""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta class."""

        model = Memberships
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at'
        )
        read_only_fields = (
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered'
        )