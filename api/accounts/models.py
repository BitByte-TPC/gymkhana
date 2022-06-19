import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from .managers import CustomUserManager

# Create your models here.

class Constants:
    BATCH = tuple((n, str(n)) for n in range(2009, datetime.datetime.now().year + 5))

    BRANCH = (
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('SM', 'Smart Manufacturing'),
        ('NS', 'Natural Sciences'),
        ('MT', 'Mechatronics'),
        ('DS', 'Design'),
        ('NA', 'Not Applicable')
    )

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    USER_TYPE = (
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('Staff', 'Staff'),
    )

    TITLE = (
        ('Prof', 'Prof'),
        ('Dr', 'Dr'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
    )

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, choices=Constants.SEX_CHOICES, default="M")
    contact_no = models.BigIntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=Constants.USER_TYPE, default="Student")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Student:
    # student info
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    batch = models.IntegerField()
    department = models.CharField(max_length=100, choices=Constants.BRANCH)
    hostel_address = models.CharField(max_length=200)
    # profile_img = models.ImageField(null=True)

    # bio
    bio = models.TextField(max_length=1000, blank=True, null=True)

    # socials
    linkedin = models.URLField(null=True, blank=True, default="www.linkedin.com")
    facebook = models.URLField(null=True, blank=True, default="www.facebook.com")
    instagram = models.CharField(null=True, blank=True, max_length=1000)
    github = models.URLField(null=True, blank=True, default="www.github.com")

class Faculty:
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices=Constants.TITLE)
    department = models.CharField(max_length=100, choices=Constants.BRANCH)
    designation = models.CharField(max_length=100, null=True)
    # profile_img = models.ImageField(null=True)

class Staff:
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # TODO: choices in department yet to be added
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    # profile_img = models.ImageField(null=True)



