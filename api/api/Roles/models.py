from accounts.models import User
from clubs.models import Club
from django.db import models


class Roles(models.Model):
    ROLE_COORDINATOR = 'Coordinator'
    ROLE_CO_COORDINATOR = 'Co-Coordinator'
    ROLE_CORE_MEMBER = 'Core member'
    ROLE_FACULTY_INCHARGE = 'Faculty Incharge'
    ROLE_CONVENER = 'Convener'
    ROLE_CO_CONVENER = 'Co-convener'
    ROLE_COUNSELLOR = ' Counsellor'
    ROLE_ASSOCIATE_COUNSELLOR = 'Associate- Counsellor'
    CLUB_ROLE_TYPES = [
        ('Coordinator', ROLE_COORDINATOR),
        ('Co-Coordinator', ROLE_CO_COORDINATOR),
        ('Core member', ROLE_CORE_MEMBER),
        ('Faculty Incharge', ROLE_FACULTY_INCHARGE),
        ('Convener', ROLE_CONVENER),
        ('Co-convener', ROLE_CO_CONVENER),
        ('Counsellor', ROLE_COUNSELLOR),
        ('Associate- Counsellor', ROLE_ASSOCIATE_COUNSELLOR)
    ]

    name = models.CharField(max_length=30, choices=CLUB_ROLE_TYPES)
    club = models.ForeignKey(Club, related_name='roles', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)
    assigned_at = models.DateField()
    active = models.BooleanField(default=True)
