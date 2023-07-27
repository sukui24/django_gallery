from django.db import models
from django.contrib.auth.models import User
import os


class ImageModel(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField()
    description = models.TextField(max_length=3000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    host = models.ForeignKey(User, max_length=100,
                             null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = os.path.basename(self.image.name)
        super().save(*args, **kwargs)
