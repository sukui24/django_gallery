from django.db import models
from django.contrib.auth.models import AbstractUser

from base.validators import FileValidator
from gallery.utils import user_avatar_path

from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


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
    avatar = ProcessedImageField(
        blank=True,
        upload_to=user_avatar_path,
        validators=[
            FileValidator(
                allowed_extensions=['jpg', 'jpeg',
                                    'png', 'webp', 'ico', 'svg'],
                allowed_mimetypes=['image/jpeg', 'image/x-png',
                                   'image/png', 'image/webp',
                                   'image/x-icon', 'image/svg+xml'],
                min_size=0,
                max_size=(5 * 1024 * 1024)
            )
        ], processors=[ResizeToFit(width=222)], options={'quality': 100},)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    def __str__(self):
        return f'id: {str(self.id)} | username: {self.username}'

    # set is_active on true after create/update user
    def save(self, *args, **kwargs):
        if not self.is_active:
            self.is_active = True
        super().save(*args, **kwargs)
