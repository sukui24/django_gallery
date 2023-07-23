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
    title = models.CharField(max_length=100)
    # tags =
    image = models.ImageField(
        null=True, blank=True, upload_to="images/", height_field="height", width_field="width")
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    # views =

    # class Meta:
    #     ordering = ['-views', '-updated', '-created']


class Comment(models.Model):

    # likes
    # dislikes
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ImageRoom, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
