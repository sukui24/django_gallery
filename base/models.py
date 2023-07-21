from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.


# class Image(models.Model):

#     link = ''

#     def __str__(self):
#         return self.link

class Tags(models.Model):

    # some tags here
    pass


class ImageRoom(models.Model):
    name = models.CharField(max_length=100)
    # tags =
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # views =

    # class Meta:
    #     ordering = ['-views', '-updated', '-created']


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ImageRoom, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
