import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import messages
from phonenumber_field.modelfields import PhoneNumberField
from users_app.models import User
from .validators import FileValidator

from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.host.id}/{filename}'


class ImageModel(models.Model):

    unique_name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=300)

    image = models.ImageField(upload_to=user_directory_path, validators=[
        FileValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'ico'],
            allowed_mimetypes=['image/jpeg', 'image/x-png',
                               'image/png', 'image/webp', 'image/x-icon'],
            max_size=(12 * 1024 * 1024)
        )
    ], blank=False, null=False)

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFit(
                                         width=550, upscale=False),],
                                     options={'quality': 90},
                                     format='JPEG')

    tags = TaggableManager(blank=True)
    is_private = models.BooleanField(default=False, blank=False, null=False)

    image_views = models.IntegerField(default=0)
    description = models.TextField(max_length=3000, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    host = models.ForeignKey(User, max_length=100,
                             null=True, on_delete=models.SET_NULL)

    # DB displaying

    def __str__(self):
        return f'id: {str(self.id)} | image: {self.image}'
