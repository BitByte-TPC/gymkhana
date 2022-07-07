from accounts.models import User
from clubs.models import Club
from django.db import models


class Roles(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starts_at = models.DateField()
    ends_at = models.DateField()
    registration_required = models.BooleanField(default=False)
    registration_approval_required = models.BooleanField(default=False)
    club = models.OneToOneField(Club, on_delete=models.SET_NULL)
    created_by = models.OneToOneField(User, on_delete=models.SET_NULL)
    address = models.TextField()
    image_url = models.URLField(max_length=500)
