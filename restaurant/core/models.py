from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)

    def __str__(self):
        return self.username

"""

class AppUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('An email is required')
        if not password:
            raise ValueError('A password is required')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('An email is required')
        if not password:
            raise ValueError('A password is required')
        user =self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user

class AppUser(AbstractUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AppUserManager()
    def __str__(self) -> str:
        return self.username
    
"""


# https://www.youtube.com/watch?v=diB38AvVkHw
# https://www.django-rest-framework.org/api-guide/authentication/
#  https://dev.to/koladev/django-rest-authentication-cmh