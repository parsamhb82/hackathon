from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


from team.serializers import (CreateInvitationSerializer,
                              CreateTeamSerializer,
                              CreateInvitationSerializer,
                              CreateTeamDemandSerializer,
                              ApplicationCreateSerializer,
                              ApplicationRejectionSerializer)

from team.models import Invitation, TeamDemand, Application 

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CreateTeamView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTeamSerializer

    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.team:
            raise ValidationError("You are already a member of a team and cannot create another one.")
        
        team = serializer.save()
        profile.team = team
        profile.save()

class InvitationCreateView(CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = CreateInvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class InvitationAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        invitation = get_object_or_404(Invitation, token=token)

        if invitation.user != request.user:
            return Response({"detail": "This invitation is not for you."}, status=status.HTTP_403_FORBIDDEN)

        if not invitation.is_open or invitation.accepted:
            return Response({"detail": "Invitation already accepted or closed."}, status=status.HTTP_400_BAD_REQUEST)

        invitation.accepted = True
        invitation.accepted_at = now()
        invitation.is_open = False
        invitation.save()

        # Optional: Add user to team logic

        return Response({"detail": "Invitation accepted successfully."}, status=status.HTTP_200_OK)
    

class CreateTeamDemandView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTeamDemandSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class CreateApplicationView(CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        demand = get_object_or_404(TeamDemand, pk=self.kwargs['pk'])
        context['demand'] = demand
        context['request'] = self.request

        return context

class AcceptApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        team = application.demand.team


        if request.user.profile.team != team:
            return Response({"detail": "You do not have permission to accept this application."}, status=status.HTTP_403_FORBIDDEN)

        if application.application_status != Application.APPLICATION_STATUS_PENDING:
            return Response({"detail": "Application has already changed"},
                            status=status.HTTP_400_BAD_REQUEST)

        application.application_status = Application.APPLICATION_STATUS_ACCEPTED
        profile = application.user.profile
        if profile.team:
            raise ValidationError("User is already a member of a team.")
        profile.team = team
        profile.save()
        application.save()

        subject = "You're application status update"
        message = (
                f"Hi {application.user.username},\n\n"
                f"The team '{application.demand.team}' has accepted your application and now you're part of their team.\n\n"
                f"Best regards,\n"
                f"Hackathon Team"
                )           

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.user.email],
            fail_silently=False,
        )

        return Response({"detail": "Application accepted successfully."}, status=status.HTTP_200_OK)

class CloseTeamDemandView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        demand = get_object_or_404(TeamDemand, pk=pk)

        if demand.team != request.user.profile.team:
            return Response({"detail": "You do not have permission to close this demand."}, status=status.HTTP_403_FORBIDDEN)

        if not demand.is_open:
            return Response({"detail": "Team demand is already closed."}, status=status.HTTP_400_BAD_REQUEST)

        demand.is_open = False
        demand.save()

        return Response({"detail": "Team demand closed successfully."}, status=status.HTTP_200_OK)


class RejectApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)

        if application.application_status != Application.APPLICATION_STATUS_PENDING:
            return Response({"detail": "Application status has already changed"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Optional: check permission
        if request.user.profile.team != application.demand.team:
            return Response({"detail": "You do not have permission to reject this application."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationRejectionSerializer(data=request.data)
        
        if serializer.is_valid():
            rejection_reason = serializer.validated_data.get('rejection_reason', '')
            subject = "You're application status update"
            message = (
                    f"Hi {application.user.username},\n\n"
                    f"The team '{application.demand.team}' has rejected your application.\n\n"
                    f"Reason: {rejection_reason}\n\n"
                    f"Best regards,\n"
                    f"Hackathon Team"
                    )           

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [application.user.email],
                fail_silently=False,
            )
            application.application_status = Application.APPLICATION_STATUS_REJECTED
            application.rejection_reason = rejection_reason
            application.save()
            return Response({"detail": "Application rejected successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)