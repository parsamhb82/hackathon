from rest_framework import serializers

from team.models import Team, TeamDemand, Invitation, Application

from user.models import UserProfile

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
    

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "name", "members", "picture", "explanation"]

    def get_members(self, obj):
        members = UserProfile.objects.filter(team=obj).select_related("user")
        return [{
            "id": user.id,
            "username": user.username,
            "email": user.email
        } for member in members if (user := member.user)]

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ["id", "user", "team", "application_status", "created_at"]

    def get_user(self, obj):
        return obj.user.username

    def get_team(self, obj):
        return obj.demand.team.name