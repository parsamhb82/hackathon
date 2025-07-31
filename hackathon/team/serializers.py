from rest_framework import serializers

from team.models import Team, Invitation

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