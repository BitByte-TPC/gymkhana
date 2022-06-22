import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

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


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):  # Add all required fields
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, choices=Constants.SEX_CHOICES, default="M")
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # user manager
    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """For cpanel."""
        self.is_active = (self.is_active is True)
        self.is_staff = (self.is_staff is True)
        self.is_superuser = (self.is_superuser is True)

        super(User, self).save(*args, **kwargs)


class Student(models.Model):
    # student info
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    roll_no = models.CharField(verbose_name='Roll No', max_length=20)
    batch = models.IntegerField()
    department = models.CharField(max_length=100, choices=Constants.BRANCH)
    hostel_address = models.CharField(verbose_name='Hostel Address', max_length=200)

    # bio
    bio = models.TextField(max_length=1000, blank=True, null=True)

    # socials
    linkedin = models.URLField(null=True, blank=True, default="www.linkedin.com")
    facebook = models.URLField(null=True, blank=True, default="www.facebook.com")
    instagram = models.CharField(null=True, blank=True, max_length=1000)
    github = models.URLField(null=True, blank=True, default="www.github.com")

    def __str__(self):
        return self.user.email


class Faculty(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices=Constants.TITLE)
    department = models.CharField(max_length=100, choices=Constants.BRANCH)
    designation = models.CharField(max_length=100, null=True)
    # profile_img = models.ImageField(null=True)

    def __str__(self):
        return self.user.email


class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # TODO: choices in department yet to be added
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    # profile_img = models.ImageField(null=True)

    def __str__(self):
        return self.user.email
