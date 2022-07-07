from accounts.models import User
from clubs.models import Club
from django.db import models


class Roles(models.Model):

    CLUB_ROLE_TYPES = [
        ('Coordinator', 'Coordinator'),
        ('Co-Coordinator', 'Co-Coordinator'),
        ('Faculty Incharge', 'Faculty Incharge'),
        ('Convener', 'Convener'),
        ('Co-convener', 'Co-convener'),
        ('Conselor', 'Conselor'),
        ('Associate-Conselor', 'Associate-Conselor')
    ]

    name = models.CharField(max_length=30, choices=CLUB_ROLE_TYPES)
    club = models.OneToOneField(Club, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_at = models.DateField()
    active = models.BooleanField(default=True)
