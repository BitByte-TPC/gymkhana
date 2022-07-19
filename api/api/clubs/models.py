from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Club (models.Model):
    CULTURAL_CLUB = 'Cultural'
    SCIENCE_AND_TECH_CLUB = 'Science & Technology'
    SPORTS_CLUB = 'Sports'

    CLUB_TYPE_CHOICES = [
        ('Cultural', CULTURAL_CLUB),
        ('S&T', SCIENCE_AND_TECH_CLUB),
        ('Sports', SPORTS_CLUB)
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=10, choices=CLUB_TYPE_CHOICES)
    description = models.TextField()
    email = models.EmailField(max_length=50, unique=True)
    logo = models.URLField(max_length=500)


class ClubRegistrationRequests(models.Model):
    class RegistrationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        APPROVED = 'Approved', _('Approved')
        REJECTED = 'Rejected', _('Rejected')

    user = models.ForeignKey(User, related_name='registration_requests', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='registration_requests', on_delete=models.CASCADE)
    fee_submitted = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=RegistrationStatus.choices,
                              default=RegistrationStatus.PENDING)
    remark = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        User, related_name='last_updated_requests',
        null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
