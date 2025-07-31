from rest_framework import serializers

from team.models import Team, Invitation, TeamDemand, Application

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

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

class CreateInvitationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    class Meta:
        model = Invitation
        fields = ['text', 'username']

    def create(self, validated_data):
        username = validated_data.pop('username')
        try:
            invited_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")

        request = self.context['request']
        team = request.user.profile.team
        sender = request.user

        invitation = Invitation.objects.create(
            team=team,
            user=invited_user,
            text=validated_data.get('text', '')
        )

        self.send_invitation_email(invitation)
        return invitation
    def send_invitation_email(self, invitation):
        #TODO use the real domain here
        accept_url = f"https://yourdomain.com{reverse('accept-invitation', args=[str(invitation.token)])}"

        subject = "You're invited to join a team!"
        message = f"""
                Hi {invitation.user.username},

                {invitation.text}

                Click the link below to accept the invitation:
                {accept_url}

                Best regards,
                Hackathon Team
            """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invitation.user.email],
            fail_silently=False,
        )

class CreateTeamDemandSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = TeamDemand
        fields = ['title', 'description']

    def create(self, validated_data):
        request = self.context['request']
        team = getattr(request.user.profile, 'team', None)
        if not team:
            raise serializers.ValidationError("You must be part of a team to create a demand.")

        team_demand = TeamDemand.objects.create(
            team=team,
            **validated_data
        )
        return team_demand
    

class ApplicationCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Application
            fields = ['motivation_text']

        def create(self, validated_data):
            user = self.context['request'].user
            demand = self.context['demand']

            return Application.objects.create(
                user=user,
                demand=demand,
                **validated_data
                )

class ApplicationRejectionSerializer(serializers.ModelSerializer):
    rejection_reason = serializers.CharField(required=False)

    class Meta:
        model = Application
        fields = ['rejection_reason']