from django.test import Client

from users_app.models import User


def create_defaultuser(client: Client) -> Client:
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
    return client


def create_superuser(client: Client) -> Client:
    """
    Input:
    - `Client` - `django.test.Client` instance

    Output:
    - `User` - `users_app.models.User` instance
    """
    User.objects.create_superuser('admin', 'foo@foo.com', 'admin')

    client.login(username='admin', password='admin')
    return client


def create_multiple_users() -> None:

    user = User.objects.create_user(
        username='testuser_1',
        password='testuser1pw'
    )
    user.first_name = 'test_1'
    user.email = 'testuser_1@gmail.com'
    user.save()

    user = User.objects.create_user(
        username='testuser_2',
        password='testuser2pw'
    )
    user.first_name = 'test_2'
    user.email = 'testuser_2@gmail.com'
    user.save()

    user = User.objects.create_user(
        username='testuser_3',
        password='testuser3pw'
    )
    user.first_name = 'test_3'
    user.email = 'testuser_3@gmail.com'
    user.save()
