from rest_framework import serializers

from team.models import Team

class CreateTeamSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Team
        fields = ['name', 'explanation', 'picture']

    def validate_picture(self, value):
        # If the client sent an empty string, treat it as no picture
        if value in ("", None):
            return None
        return value
    
