from django.urls import path
from team.views import CreateTeamView, InvitationAcceptView, InvitationCreateView

urlpatterns = [
    path('create/', CreateTeamView.as_view(), name='create-team'),
    path('invitations/create/', InvitationCreateView.as_view(), name='create-invitation'),
    path('invitations/accept/<uuid:token>/', InvitationAcceptView.as_view(), name='accept-invitation'),
]