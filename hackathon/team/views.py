from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from team.serializers import CreateTeamSerializer, CreateInvitationSerializer
from team.models import Invitation

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CreateTeamView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTeamSerializer

    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.team:
            raise ValidationError("You are already a member of a team and cannot create another one.")
        
        team = serializer.save()
        profile.team = team
        profile.save()

class InvitationCreateView(CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = CreateInvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class InvitationAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        invitation = get_object_or_404(Invitation, token=token)

        if invitation.user != request.user:
            return Response({"detail": "This invitation is not for you."}, status=status.HTTP_403_FORBIDDEN)

        if not invitation.is_open or invitation.accepted:
            return Response({"detail": "Invitation already accepted or closed."}, status=status.HTTP_400_BAD_REQUEST)

        invitation.accepted = True
        invitation.accepted_at = now()
        invitation.is_open = False
        invitation.save()

        # Optional: Add user to team logic

        return Response({"detail": "Invitation accepted successfully."}, status=status.HTTP_200_OK)