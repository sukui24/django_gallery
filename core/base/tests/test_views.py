import os
import shutil

from django.test import Client, TestCase
from django.urls import reverse

from gallery.settings import BASE_DIR

from base.models import ImageModel
from users_app.models import User
from .utils import create_image, create_superuser


class TestViewsWithPk(TestCase):

    __slots__ = ['delete_image_url', 'edit_image_url', 'client']

    def setUp(self):
        self.client = Client()
        self.delete_image_url = reverse('delete-image', args=['1'])
        self.edit_image_url = reverse('edit-image', args=['1'])

    def test_edit_image_POST(self):
        """
        => test_views => TestViewsWithoutPk

        Test image editing `POST` request

        Edited fields:
        `title`: "images" => "edited_title"
        `is_private`: False => True
        `description`: "" => "Added description"
        """
        image = create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        response = self.client.post(self.edit_image_url, {
            'id': 1,
            'title': 'edited_title',
            'is_private': True,
            'description': 'Added description'
        })

        image = ImageModel.objects.get(pk=1)

        # checking that rest fields are same as before editing
        # 302 cause we get redirect after posting image
        self.assertEquals(response.status_code, 302)
        self.assertEquals(image.id, 1)
        self.assertEquals(image.image.url.split('/')[-1], 'test_image.jpg')
        self.assertEquals(image.host.id, 1)
        self.assertEquals(image.unique_name, 'test_image.jpg')
        # changed fields
        self.assertEquals(image.description, 'Added description')
        self.assertEquals(image.title, 'edited_title')
        self.assertEquals(image.is_private, True)

    def test_delete_image_POST(self):
        """
        => test_views => TestViewsWithPk
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        response = self.client.post(self.delete_image_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(ImageModel.objects.count(), 0)

    def test_delete_image_POST_unlogged_in(self):
        """
        => test_views => TestViewsWithPk
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)
        self.client.logout()

        response = self.client.post(self.delete_image_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(ImageModel.objects.count(), 1)

    def test_delete_image_POST_wrong_id(self):
        """
        => test_views => TestViewsWithPk
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        self.delete_image_url = reverse('delete-image', args=['9999'])
        response = self.client.post(self.delete_image_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(ImageModel.objects.count(), 1)


class TestViewsWithoutPk(TestCase):
    """
    For test cases i setted default storages variables, you can
    see it in gallery/settings.py

    `...WithoutPk` means there's no pk in link. Just splitted on this
    two classes for better readability
    """
    __slots__ = ['client', 'home_url', 'add_image_url',]

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.add_image_url = reverse('add-image')

    @classmethod
    def tearDownClass(cls):
        """
        Deleting useless folders that makes by signals
        """
        user_path = os.path.join(BASE_DIR, "base/tests/test_images/user_1")
        cache_path = os.path.join(BASE_DIR, "base/tests/test_images/CACHE")

        if os.path.exists(user_path):
            shutil.rmtree(user_path)

        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
        super().tearDownClass()

    def test_home_GET_with_image(self):
        """
        => test_views => TestViewsWithoutPk
        """
        create_image(self.client)
        self.assertEquals(ImageModel.objects.count(), 1)

        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_add_image_POST(self):
        """
        => test_views => TestViewsWithoutPk

        On start:
        - No User account
        - No ImageModel instances

        In test process:
        - Created superuser and set him as host of an image
        - Created image using `POST` request
        - Assigned image variable after creating due to `post_save`
            unique_name setter signal
        """
        host = create_superuser(self.client)
        self.assertEquals(User.objects.count(), 1)

        image_path = os.path.join(
            BASE_DIR, 'base/tests/test_images/test_add_image.jpg')

        with open(image_path, "rb") as image:
            response = self.client.post(self.add_image_url, {
                'id': 1,
                'title': 'images',
                'image': image,
                'host': host,
                'is_private': False,
                'description': ''
            },)

        image = ImageModel.objects.get(pk=1)

        # code 302 cause we get redirected after creating image
        self.assertEquals(response.status_code, 302)
        self.assertEquals(image.title, 'images')
        self.assertEquals(image.unique_name, 'test_add_image.jpg')

    def test_add_image_POST_no_data(self):
        """
        => test_views => TestViewsWithoutPk
        """
        response = self.client.post(self.add_image_url, {})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.content, b'')
        self.assertEquals(ImageModel.objects.count(), 0)

    def test_for_properly_tags_adding_POST_creating(self):
        """
        => test_views => TestViewsWithoutPk
        """
        host = create_superuser(self.client)

        image_path = os.path.join(BASE_DIR,
                                  'base/tests/test_images/test_image.jpg')

        # in `taggit` every tag is a instance of model `Tag`
        # that means we cannot send more that one tag in our request
        # while we do so in form, `taggit` convert every `str` in instance of `Tag`
        with open(image_path, 'rb') as image:
            response = self.client.post(self.add_image_url, {
                "id": 1,
                "title": 'tags_testing',
                "image": image,
                "host": host,
                "tags": "123"
            })
        # code 302 cause we do redirect after image posting
        self.assertEquals(response.status_code, 302)
        self.assertEquals(ImageModel.objects.count(), 1)

        # on prod for some reason DB works differently from local dev
        # so we will get last created image (usually it's id=2)
        image = ImageModel.objects.latest('id')
        self.assertEquals(image.tags.count(), 1)

        image.tags.add("some new tag")
        self.assertEquals(image.tags.count(), 2)

        image.tags.remove("123")
        self.assertEquals(image.tags.count(), 1)

        image.tags.remove("some new tag")
        self.assertEquals(image.tags.count(), 0)

        response = image.tags.remove("some unreal tag")
        self.assertEquals(response, None)
