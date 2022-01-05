"""Circle memberships views."""

# Django Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import status

# Local
from cride.circles.permissions.memberships import IsActiveCircleMember, IsSelfMember
from cride.circles.serializers.memberships import MembershipsModelSerializer, AddMemberSerializer
from cride.circles.models.circles import Circle
from cride.circles.models.memberships import Memberships
from cride.circles.models.invitations import Invitation

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
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
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveCircleMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
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

    @action(detail=True, methods=['GET'])
    def invitations(self, request, *args, **kwargs):
        """Retrieve a member's invitations breakdown.

        Will return a list containing all the members that have
        used its invitations and another list containing the
        invitations that haven't being used yet.
        """
        member = self.get_object()
        invited_members = Memberships.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False
        ).values_list('code')

        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code
            )

        data = {
            'used_invitations': MembershipsModelSerializer(invited_members, many=True),
            'invitations': invitations
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(
            data=request.data,
            context={'circle': self.circle, 'request': request}
        )
        serializer.is_valid(raise_exceptrion=True)
        member = serializer.save()
        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)