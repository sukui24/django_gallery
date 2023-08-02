from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.contrib import messages


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.host.id}/{filename}'

# in future way better would be initialize user method first and give it image argument
# which will be ForeignKey. This means each user will have their images, not like rn
# images have user (owner). That's ok but kinda not rigth :p


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=60, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(max_length=2000, null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


# /// TODO: if unique name - add random symbols
class ImageModel(models.Model):

    unique_name = models.CharField(max_length=100, unique=True, null=True)
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to=user_directory_path)

    description = models.TextField(max_length=3000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    host = models.ForeignKey(User, max_length=100,
                             null=True, on_delete=models.SET_NULL)

    # ? i don't like this flags idea but right now idk how to
    # ? make this without flag if it even possibe so ...
    image_flag = models.BooleanField(default=False)

    # * overriding save method for ImageModel
    def save(self, *args, **kwargs):

        # scanning if directory is empty and just save if it is
        if not any(os.scandir(f'./media/images/user_{self.host.id}')):
            self.unique_name = os.path.basename(self.image.name)
            self.image_flag = False
            super().save(*args, **kwargs)

        # * if we edit or create the actual image we add all params
        # * or just save evetyrhing if we're not
        elif self.image_flag:
            # getting future object id (last id + 1)
            LastInsertId = (ImageModel.objects.last()).id + 1
            # making unique image name to avoid errors
            self.image.name = str(LastInsertId) + '_' + self.image.name
            # declare the unique_name variable to use it in future
            self.unique_name = os.path.basename(self.image.name)
            self.image_flag = False
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

# * overriding delete method for ImageModel
    def delete(self, *args, **kwargs):
        # removing image from media root
        os.remove('./media/images/' + self.image.name)
        super().delete(*args, **kwargs)

    # displaying image.name in DB
    def __str__(self):
        return self.image.name
