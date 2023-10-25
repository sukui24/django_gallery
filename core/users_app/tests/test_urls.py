from django.test import TestCase, Client
from django.urls import reverse

from .utils import create_defaultuser, create_superuser


class TestUrlsWithoutPk(TestCase):

    __slots__ = ['client', 'register_url', 'logout_url', 'login_url']

    def setUp(self) -> None:
        self.client = Client()
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.login_url = reverse('login')

    def test_register_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithoutPk
        """
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)

    def test_logout_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithoutPk
        """
        response = self.client.get(self.logout_url)

        # code 302 cause we get redirect after logout
        self.assertEquals(response.status_code, 302)

    def test_login_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithoutPk
        """
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)


class TestUrlsWithPkGetRequests(TestCase):

    __slots__ = ['client', 'profile_url', 'edit_user_url', 'user_images_url',
                 'user_images_private_url', 'delete_account_url']

    def setUp(self) -> None:
        self.client = Client()
        self.profile_url = reverse('profile', args=['1'])
        self.edit_user_url = reverse('edit-user', args=['1'])
        self.user_images_url = reverse('user-images', args=['1'])
        self.user_images_private_url = reverse(
            'user-images-private', args=['1'])
        self.delete_account_url = reverse('delete-account', args=['1'])

    def test_profile_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithPkGetRequests
        """
        response = self.client.get(self.profile_url)

        # there's no users so status code 404
        self.assertEquals(response.status_code, 404)

        self.client = create_defaultuser(self.client)

        response = self.client.get(self.profile_url)

        # code 200 cause now users exists
        self.assertEquals(response.status_code, 200)

    def test_edit_user_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithPkGetRequests
        """
        self.client = create_defaultuser(self.client)  # user_1
        self.client.logout()
        self.client = create_superuser(self.client)  # user_2

        # as user_2 we trying to get access to edit user_1
        response = self.client.get(self.edit_user_url)

        # system redirect us if we have no permission
        self.assertEquals(response.status_code, 302)

        self.edit_user_url = reverse('edit-user', args=['2'])

        response = self.client.get(self.edit_user_url)

        # now we trying to edit our account so code is 200
        self.assertEquals(response.status_code, 200)

    def test_user_images_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithPkGetRequests
        """
        self.client = create_defaultuser(self.client)

        response = self.client.get(self.user_images_url)

        self.assertEquals(response.status_code, 200)

    def test_user_images_private_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithPkGetRequests
        """
        self.client = create_defaultuser(self.client)  # user_1
        self.client.logout()
        self.client = create_superuser(self.client)  # user_2

        response = self.client.get(self.user_images_private_url)

        # redirect if we have no permissions
        self.assertEquals(response.status_code, 302)

        self.user_images_private_url = reverse(
            'user-images-private', args=['2'])

        response = self.client.get(self.user_images_private_url)

        # code 200 cause it's our images now
        self.assertEquals(response.status_code, 200)

    def test_delete_account_url_GET(self) -> None:
        """
        Located in: users_app => tests => test_urls =>  TestUrlsWithPkGetRequests
        """
        self.client = create_defaultuser(self.client)  # user_1
        self.client.logout()
        self.client = create_superuser(self.client)  # user_2

        response = self.client.get(self.delete_account_url)

        # redirect cause has no permissions
        self.assertEquals(response.status_code, 302)

        self.delete_account_url = reverse('delete-account', args=['2'])

        response = self.client.get(self.delete_account_url)

        # code 200 cause it's our account
        self.assertEquals(response.status_code, 200)
