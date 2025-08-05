from team.models import Team, TeamDemand, Application, Invitation
from team.list_get_serializers import TeamDemandSerializer, InvitationSerializer

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class TeamDemandListView(ListAPIView):
    queryset = TeamDemand.objects.filter(is_open=True)
    serializer_class = TeamDemandSerializer

class InvitationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(team=user.profile.team)