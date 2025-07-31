from django.urls import path
from team.views import (CreateTeamView,
                        InvitationAcceptView,
                        InvitationCreateView,
                        CreateTeamDemandView,
                        CreateApplicationView,
                        AcceptApplicationView,
                        CloseTeamDemandView)

urlpatterns = [
    path('create/', CreateTeamView.as_view(), name='create-team'),
    path('invitations/create/', InvitationCreateView.as_view(), name='create-invitation'),
    path('invitations/accept/<uuid:token>/', InvitationAcceptView.as_view(), name='accept-invitation'),
    path('demands/create/', CreateTeamDemandView.as_view(), name='create-team-demand'),
    path('demands/<int:pk>/apply/', CreateApplicationView.as_view(), name='apply-to-demand'),
    path('applications/<int:pk>/accept/', AcceptApplicationView.as_view(), name="accept-application"),
    path('demands/<int:pk>/close/', CloseTeamDemandView.as_view(), name="close-team-demand")
]