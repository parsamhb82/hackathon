from django.shortcuts import render

from team.serializers import CreateTeamSerializer

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

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