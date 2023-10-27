from django.test import TestCase, Client
from django.urls import reverse

from users_app.models import User

from .fixtures import create_defaultuser, create_superuser, create_multiple_users


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.edit_user_url = reverse('edit-user', args=['1'])
        self.delete_account_url = reverse('delete-account', args=['1'])

    def test_edit_user_POST(self) -> None:
        """
        Located in: users_app => tests => test_views =>  TestUrlsWithPkPostRequests

        User data before edit:
        first_name = "testuser",
        username = "testuser",
        email = "testuser@gmail.com",
        password = "defaultuser1234"
        """

        self.client = create_defaultuser(self.client)

        self.assertEquals(User.objects.count(), 1)

        response = self.client.post(self.edit_user_url, {
            "first_name": "edited_testuser",
            "username": "edited_username",
            "email": "edited_testuser@gmail.com",
        })

        user = User.objects.get(pk=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(user.first_name, "edited_testuser")
        self.assertEquals(user.username, "edited_username")
        self.assertEquals(user.email, "edited_testuser@gmail.com")

    def test_edit_user_without_permission_POST(self) -> None:
        """
        Located in: users_app => tests => test_views =>  TestUrlsWithPkPostRequests

        User data before edit:
        first_name = "testuser",
        username = "testuser",
        email = "testuser@gmail.com",
        password = "defaultuser1234"
        """
        self.client = create_defaultuser(self.client)
        self.client.logout()
        self.client = create_superuser(self.client)
        self.assertEquals(User.objects.count(), 2)

        # try to edit someone's account
        response = self.client.post(self.edit_user_url, {
            "first_name": "edited_testuser",
            "username": "edited_username",
            "email": "edited_testuser@gmail.com",
        })
        self.assertEquals(response.status_code, 302)

        # redirect cause we can't edit other ppl accounts
        # all fields stay the same
        user = User.objects.get(pk=1)
        self.assertEquals(user.first_name, "testuser")
        self.assertEquals(user.username, "testuser")
        self.assertEquals(user.email, "testuser@gmail.com")

    def test_delete_account_POST(self) -> None:
        """
        Located in: users_app => tests => test_views =>  TestUrlsWithPkPostRequests
        """
        self.client = create_defaultuser(self.client)

        self.assertEquals(User.objects.count(), 1)

        response = self.client.post(self.delete_account_url)

        # redirect after account deletion
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 0)

    def test_delete_account_without_permission_POST(self) -> None:
        """
        Located in: users_app => tests => test_views =>  TestUrlsWithPkPostRequests
        """
        self.client = create_defaultuser(self.client)
        self.client.logout()
        self.client = create_superuser(self.client)

        self.assertEquals(User.objects.count(), 2)

        response = self.client.post(self.delete_account_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 2)

    def test_multiple_users_create_properly(self) -> None:
        """
        Located in: users_app => tests => test_views =>  TestUrlsWithPkPostRequests
        """
        create_multiple_users()

        self.assertEquals(User.objects.count(), 3)

        self.assertIsNotNone(User.objects.get(pk=1))
        self.assertIsNotNone(User.objects.get(pk=2))
        self.assertIsNotNone(User.objects.get(pk=3))
