from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(('Users must have an username address'))
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    class Meta:
        permissions= (("tier_1", "Can view 3 suggestions"), ("tier_2", "Can view 6 suggestions"),
        # You can add other custom permissions as required
        )
    

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
        
    )

    ROLE = (
        ('none','none'),
        ('waiters', 'waiters'),
        ('kitchen', 'kitchen'),
        ('manager', 'manager'),
        ('owner', 'owner')
    )

    email = models.EmailField(unique=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    role = models.CharField(max_length=100, choices=ROLE, default='none')
    description = models.TextField("Description", max_length=600, default='', blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username





"""
"""


# https://www.youtube.com/watch?v=diB38AvVkHw
# https://www.django-rest-framework.org/api-guide/authentication/
#  https://dev.to/koladev/django-rest-authentication-cmh