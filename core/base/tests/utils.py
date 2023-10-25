import os

from gallery.settings import BASE_DIR

from django.test import Client

from base.models import ImageModel
from users_app.models import User


def create_superuser(client: Client) -> User:
    """
    Input:
    - `Client` - `django.test.Client` instance

    Output:
    - `User` - `users_app.models.User` instance
    """
    user = User.objects.create_superuser('admin', 'foo@foo.com', 'admin')

    client.login(username='admin', password='admin')
    return user


def create_image(client: Client) -> ImageModel:
    """
    Input:
    - `Client` - `django.test.Client` instance

    Output:
    - `ImageModel` - `base.models.ImageModel` instance
    """
    host = create_superuser(client)
    image_path = os.path.join(
        BASE_DIR, 'base/tests/test_images/test_image.jpg')
    image = ImageModel.objects.create(
        id=1,
        title='images',
        image=image_path,
        host=host
    )
    return image
