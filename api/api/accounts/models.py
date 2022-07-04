import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


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


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Constants.SEX_CHOICES, default="M")
    contact_no = models.BigIntegerField(verbose_name='Contact No', null=True, blank=True)
    user_type = models.CharField(
        verbose_name='User Type',
        max_length=50,
        choices=Constants.USER_TYPE,
        default="Student"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    picture_url = models.URLField(max_length=500)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)


class Student(models.Model):
    # student info
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    roll_no = models.CharField(verbose_name='Roll No', max_length=20)
    batch = models.IntegerField()
    department = models.CharField(max_length=100, choices=Constants.BRANCH)
    hostel_address = models.CharField(verbose_name='Hostel Address', max_length=200)
    bio = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.user.email


class Faculty(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices=Constants.TITLE)
    department = models.CharField(max_length=100, choices=Constants.BRANCH)
    designation = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.email


class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # TODO(#83): add choices in department to which staff belongs to
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email


class StudentSocial(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.CharField(null=True, blank=True, max_length=100)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.email
