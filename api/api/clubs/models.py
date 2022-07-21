from decimal import Decimal

from django.db import models


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
    registration_open = models.BooleanField(default=False)
    fee_required = models.BooleanField(default=False)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
