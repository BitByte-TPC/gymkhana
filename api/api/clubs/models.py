from django.contrib.auth import get_user_model
from django.db import models

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
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        ('Pending', STATUS_PENDING),
        ('Approved', STATUS_APPROVED),
        ('Rejected', STATUS_REJECTED)
    ]

    user = models.ForeignKey(User, related_name='registered_clubs', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='registration_requests', on_delete=models.CASCADE)
    fee_submitted = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    remark = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        User, related_name='updated_club_registration_requests',
        null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
