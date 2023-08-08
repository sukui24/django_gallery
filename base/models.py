from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.contrib import messages
from phonenumber_field.modelfields import PhoneNumberField
import fnmatch
from users_app.models import User


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.host.id}/{filename}'


class ImageModel(models.Model):

    unique_name = models.CharField(max_length=100, unique=True, null=True)
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to=user_directory_path)

    description = models.TextField(max_length=3000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    host = models.ForeignKey(User, max_length=100,
                             null=True, on_delete=models.SET_NULL)

    # displaying image.name in DB

    def __str__(self):
        return self.image.name
