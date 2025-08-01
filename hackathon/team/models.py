from django.db import models
from django.contrib.auth.models import User
import uuid


class Team(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="team_pictures/", blank=True, null=True)

    def __str__(self):
        return self.name

class Invitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations")
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 


    def save(self, *args, **kwargs):

        if not self.text and self.team_id:  # if text is not set, generate it
            self.text = f"Team {self.team.name} wants you to join for the upcoming event"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation to {self.team.name} for {self.user.username}"

class TeamDemand(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="demands")
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.description and self.team_id:  # if description is not set, generate it
            self.description = f"Team {self.team.name} is looking for a {self.title}."
    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"team demand  {self.team.name} for {self.title}, pk:{self.id}"

class Application(models.Model):
    APPLICATION_STATUS_PENDING = 1
    APPLICATION_STATUS_ACCEPTED = 2
    APPLICATION_STATUS_REJECTED = 3

    APPLICATION_STATUS_CHOICES = [
        (APPLICATION_STATUS_PENDING, "Pending"),
        (APPLICATION_STATUS_ACCEPTED, "Accepted"),
        (APPLICATION_STATUS_REJECTED, "Rejected"),
    ]

    demand = models.ForeignKey(TeamDemand, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    motivation_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    application_status = models.PositiveSmallIntegerField(choices=APPLICATION_STATUS_CHOICES, default=APPLICATION_STATUS_PENDING)

    def __str__(self):
        return f"Application for {self.demand.title} by {self.user.username} with id:{self.id}"