from django.test import TestCase, Client

from users_app.models import User

from .utils import create_defaultuser


class TestModel(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_is_active_using_create(self) -> None:
        """
        Located in: users_app => tests => test_models =>  TestModel
        """
        User.objects.create(
            first_name="test",
            username="test",
            email="test",
            password="testuser123"
        )
        user = User.objects.get(pk=1)
        self.assertEquals(User.objects.count(), 1)
        self.assertTrue(user.is_active)

    def test_is_active_usint_create_user(self) -> None:
        """
        Located in: users_app => tests => test_models =>  TestModel
        """
        create_defaultuser(self.client)
        user = User.objects.get(pk=1)

        self.assertEquals(User.objects.count(), 1)
        self.assertTrue(user.is_active)
