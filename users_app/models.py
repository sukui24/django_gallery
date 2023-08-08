from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


def user_avatar_path(instance, filename):
    future_id = (User.objects.last().id) + 1
    return f'user_{future_id}/{filename}'


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(unique=True, max_length=60, null=True)

    phone_number = PhoneNumberField(blank=True)
    city = models.CharField(max_length=187, blank=True)
    country = models.CharField(max_length=56, blank=True)
    adress = models.CharField(max_length=70, blank=True)
    email = models.EmailField(unique=True)

    bio = models.TextField(max_length=8000, null=True, blank=True)
    avatar = models.ImageField(
        upload_to=user_avatar_path, default="avatar.svg")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    def __str__(self):
        return self.username
