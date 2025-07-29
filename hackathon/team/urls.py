from django.urls import path
from team.views import CreateTeamView

urlpatterns = [
    path('create/', CreateTeamView.as_view(), name='create-team'),
]