from rest_framework import serializers

from team.models import Team, TeamDemand, Invitation, Application

class TeamDemandSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = TeamDemand
        fields = ["id", "team", "title", "description", "created_at"]

    def get_team(self, obj):
        return obj.team.name

class InvitationSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ["id", "team", "created_at", "username", "text"]

    def get_team(self, obj):
        return obj.team.name

    def get_username(self, obj):
        return obj.user.username
