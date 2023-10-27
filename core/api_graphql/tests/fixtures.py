import os

from gallery.settings import BASE_DIR

from django.test import Client

from base.models import ImageModel
from users_app.models import User

from users_app.tests.fixtures import create_multiple_users \
    as users_app_create_multiple_users


class MockUser:
    """
    > Using only in `MockContext` <
    """
    __slots__ = ['id', 'is_staff', 'is_authenticated_value']

    def __init__(self, user: User, is_authenticated: bool):
        self.id = user.id
        self.is_staff = user.is_staff
        self.is_authenticated_value = is_authenticated

    @property
    def is_authenticated(self):
        return self.is_authenticated_value


class MockContext:
    """
    Mock context used as context in GraphQL mutations

    This mock context have all fields that used somewhere as dummies
    But i left here ability to set variables in case you need to
    """
    __slots__ = ['user', 'method', 'FILES']

    def __init__(self,
                 is_authenticated: bool = True,
                 user: User = None,
                 method='GET',
                 FILES=''):
        """
        FILES is just `info.context` argument, but we always send just one file
        """
        if user is not None:
            self.user = MockUser(user, is_authenticated)
        else:
            self.user = ''
        self.method = method
        self.FILES = FILES


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


def create_defaultuser(client: Client) -> User:
    """
    Input:
    - `Client` - `django.test.Client` instance

    Output:
    - `User` - `users_app.models.User` instance
    """
    user = User.objects.create_user(
        username="testuser",
        password="defaultuser1234"
    )
    user.first_name = "testuser"
    user.email = "testuser@gmail.com"
    user.save()

    client.login(username='testuser', password='defaultuser1234')
    return user


def create_multiple_users() -> None:
    """
    Reusing already existing fucntion for creating multiple users

    Didn't do the same for other cause fixtures in `users_app` returns `Client`
    instance, but we need `User` instance in this tests
    """
    users_app_create_multiple_users()


def create_image(client: Client) -> ImageModel:
    """
    Input:
    - `Client` - `django.test.Client` instance

    Output:
    - `ImageModel` - `base.models.ImageModel` instance
    """
    host = create_superuser(client)
    image_path = os.path.join(
        BASE_DIR, 'api_graphql/tests/test_images/test_image.jpg')
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
        BASE_DIR, 'api_graphql/tests/test_images/test_image.jpg')
    image_path_2 = os.path.join(
        BASE_DIR, 'api_graphql/tests/test_images/test_image_2.jpg')
    image_path_3 = os.path.join(
        BASE_DIR, 'api_graphql/tests/test_images/test_image_3.jpg')

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
