
from django.test import Client, TestCase
from django.urls import reverse

from base.models import ImageModel
from users_app.models import User

from .fixtures import create_image, create_superuser


class TestUrlsStatic(TestCase):
    """
    Static urls means urls without `pk`
    """

    def setUp(self) -> None:
        self.client = Client()
        self.home_url = reverse('home')
        self.add_image_url = reverse('add-image')

    def test_home_url_GET(self) -> None:
        """
        Located in: base => tests => test_urls => TestUrlsStatic
        """
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_add_image_GET(self) -> None:
        """
        Located in: base => tests => test_urls => TestUrlsStatic
        """
        response = self.client.get(self.add_image_url)

        # code 302(redirect) because user unlogged-in and has no permissions
        self.assertEquals(response.status_code, 302)

        create_superuser(self.client)
        self.assertEquals(User.objects.count(), 1)

        response = self.client.get(self.add_image_url)

        # code 200 because user logged-in
        self.assertEquals(response.status_code, 200)


class TestUrlsDynamic(TestCase):
    """
    Dynamic urls means urls with `pk`
    """

    def setUp(self) -> None:
        self.client = Client()
        self.view_image_url = reverse('view-image', args=['1'])
        self.edit_image_url = reverse('edit-image', args=['1'])
        self.download_image_url = reverse('download-image', args=['1'])

    def test_edit_image_GET(self) -> None:
        """
        Located in: base => tests => test_urls => TestUrlsDynamic
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        response = self.client.get(self.edit_image_url)

        # code 200 because user logged-in
        self.assertEquals(response.status_code, 200)

        self.client.logout()

        response = self.client.get(self.edit_image_url)

        # code 302(redirect) because user unlogged-in and has no permissions
        self.assertEquals(response.status_code, 302)

    def test_view_image_GET(self) -> None:
        """
        Located in: base => tests => test_urls => TestUrlsDynamic
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        response = self.client.get(self.view_image_url)

        self.assertEquals(response.status_code, 200)

    def test_download_image_GET(self) -> None:
        """
        Located in: base => tests => test_urls => TestUrlsDynamic
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)
        response = self.client.get(self.download_image_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response).__name__, 'FileResponse')
        self.assertEquals(type(response.streaming_content).__name__, 'map')

    def test_download_image_GET_wrong_pk(self) -> None:
        """
        Located in: base => tests => test_urls => TestUrlsDynamic
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        self.download_image_url = reverse('download-image', args=['9999'])
        response = self.client.get(self.download_image_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(ImageModel.objects.count(), 1)
