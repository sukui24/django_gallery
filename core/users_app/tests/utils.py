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
