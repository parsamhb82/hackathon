from django.urls import path
from team.views import CreateTeamView, InvitationAcceptView, InvitationCreateView, CreateTeamDemandView

urlpatterns = [
    path('create/', CreateTeamView.as_view(), name='create-team'),
    path('invitations/create/', InvitationCreateView.as_view(), name='create-invitation'),
    path('invitations/accept/<uuid:token>/', InvitationAcceptView.as_view(), name='accept-invitation'),
    path('demands/create/', CreateTeamDemandView.as_view(), name='create-team-demand'),
]