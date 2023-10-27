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


def create_multiple_images(client: Client) -> None:
    """
    Created 3 images for current test session, but didn't return anything
    """
    host = create_superuser(client)

    image_path_1 = os.path.join(
        BASE_DIR, 'base/tests/test_images/test_image.jpg')
    image_path_2 = os.path.join(
        BASE_DIR, 'base/tests/test_images/test_image_2.jpg')
    image_path_3 = os.path.join(
        BASE_DIR, 'base/tests/test_images/test_image_3.jpg')

    ImageModel.objects.create(
        title='test_image_1',
        image=image_path_1,
        host=host
    )
    ImageModel.objects.create(
        title='test_image_2',
        image=image_path_2,
        host=host
    )
    ImageModel.objects.create(
        title='test_image_3',
        image=image_path_3,
        host=host
    )
