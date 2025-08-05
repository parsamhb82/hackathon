from django.contrib import admin
from team.models import Team, TeamDemand, Invitation, Application

admin.site.register(Team)
admin.site.register(Invitation)
admin.site.register(TeamDemand)
admin.site.register(Application)
