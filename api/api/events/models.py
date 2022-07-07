from accounts.models import User
from clubs.models import Club
from django.db import models


class Events(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starts_at = models.DateField()
    ends_at = models.DateField()
    registration_required = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, null=True, related_name='events_created', on_delete=models.SET_NULL)
    image_url = models.URLField(max_length=500)
    # This club is the primary organizer of this event
    club = models.ForeignKey(Club, related_name='events', on_delete=models.PROTECT)
    registration_approval_required = models.BooleanField(default=False)
    address = models.CharField(max_length=500)
