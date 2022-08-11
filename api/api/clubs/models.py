from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Club (models.Model):
    class ClubType(models.TextChoices):
        CULTURAL = 'Cultural', _('Cultural')
        SCIENCE_AND_TECH = 'S&T', _('Science & Technology')
        SPORTS = 'Sports', _('Sports')

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=10, choices=ClubType.choices)
    description = models.TextField()
    email = models.EmailField(max_length=50, unique=True)
    logo = models.URLField(max_length=500)
    slug = models.SlugField(unique=True)
    registration_open = models.BooleanField(default=False)
    fee_required = models.BooleanField(default=False)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    registration_deadline = models.DateTimeField(blank=True, null=True)


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
