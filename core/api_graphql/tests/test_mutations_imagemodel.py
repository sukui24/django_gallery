from django.test import TestCase, Client
from api_graphql.schemas import schema
from graphene.test import Client as GraphQLClient
from .fixtures import (
    create_image,
    MockContext,
    create_multiple_images,
    create_defaultuser
)
from base.models import ImageModel
from users_app.models import User
from gallery.settings import BASE_DIR
import os


class ImageModelCreateMutations(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.query = """
        mutation ($title: String!, $isPrivate: Boolean!){
            createImage(input_: {title: $title, isPrivate: $isPrivate}) {
                data {
                id
                title
                image
                isPrivate
                }
            }
        }
        """

    def test_image_creation_without_image_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => ImageModelCreateMutations
        """
        create_defaultuser(self.django_client)
        self.assertEquals(User.objects.count(), 1)

        user = User.objects.get(pk=1)

        self.assertEquals(ImageModel.objects.count(), 0)

        values = {"title": "123", "isPrivate": False}
        context = MockContext(user=user, method='POST')
        response = self.client.execute(
            self.query,
            variable_values=values,
            context=context
        )
        self.assertIsNotNone(response)

        expected_response = "{'errors': [{'message': 'Image was not provided in the POST request', 'locations': [{'line': 3, 'column': 13}], 'path': ['createImage']}], 'data': {'createImage': None}}"

        self.assertEquals(str(response), expected_response)

    def test_image_creation_unlogged_in_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => ImageModelCreateMutations
        """
        create_defaultuser(self.django_client)
        self.assertEquals(User.objects.count(), 1)
        user = User.objects.get(pk=1)

        image_path = os.path.join(
            BASE_DIR, 'api_graphql/tests/test_images/test_image.jpg')

        image = {'0': image_path}
        context = MockContext(user=user, method='POST',
                              FILES=image, is_authenticated=False)

        values = {"title": "123", "isPrivate": False}
        response = self.client.execute(
            self.query,
            variable_values=values,
            context=context
        )
        self.assertIsNotNone(response)

        expected_response = "{'errors': [{'message': 'Only authenticated users can upload images', \
'locations': [{'line': 3, 'column': 13}], 'path': ['createImage']}], 'data': {'createImage': None}}"

        self.assertEquals(str(response), expected_response)


class TestImageModelMutations(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.update_query = """
        mutation ($id: ID, $title: String){
            updateImage(id: $id, input_: {title: $title}) {
                success
                data {
                title
                }
            }
        }"""
        self.deletion_query = """
        mutation ($id:ID) {
            deleteImage(id: $id) {
                success
            }
        }
        """

    def test_image_delete_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => TestImageModelMutations
        """
        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)

        user = User.objects.latest('id')

        context = MockContext(user=user, method='POST')
        response = self.client.execute(
            self.deletion_query,
            variable_values={'id': 1},
            context=context
        )
        self.assertIsNotNone(response)

        expected_response = "{'data': {'deleteImage': {'success': True}}}"

        self.assertEquals(str(response), expected_response)

    def test_image_delete_without_permission_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => TestImageModelMutations

        Be careful in changing this test. If you're changing query, then response
        could change for example in `'location'` parameter
        """

        create_multiple_images(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 3)

        create_defaultuser(self.django_client)
        # 4 users cause `create_multiple_images` creates user as well
        self.assertEquals(User.objects.count(), 2)

        user = User.objects.get(pk=2)

        context = MockContext(user=user, method='POST')
        response = self.client.execute(
            self.deletion_query,
            variable_values={'id': 1},
            context=context
        )
        self.assertIsNotNone(response)

        expected_response = "{'errors': [{'message': 'Only image host can delete it', \
'locations': [{'line': 3, 'column': 13}], 'path': ['deleteImage']}], 'data': {'deleteImage': None}}"

        self.assertEquals(str(response), expected_response)

    def test_update_image_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => TestImageModelMutations

        Image before updating:
        - title= 'images'

        Image after updating:
        - title = 'updated_image_title'
        """

        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)
        user = User.objects.latest('id')

        values = {"id": "1", "title": "updated_image_title"}
        context = MockContext(user=user, method='POST')
        response = self.client.execute(
            self.update_query,
            variable_values=values,
            context=context
        )

        self.assertIsNotNone(response)

        expected_response = "{'data': {'updateImage': {'success': True, 'data': {'title': 'updated_image_title'}}}}"

        self.assertEquals(str(response), expected_response)

    def test_update_image_without_permission_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => TestImageModelMutations
        """
        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)

        create_defaultuser(self.django_client)
        self.assertEquals(User.objects.count(), 2)

        user = User.objects.get(pk=2)

        values = {"id": "1", "title": "updated_image_title"}
        context = MockContext(user=user, method='POST')
        response = self.client.execute(
            self.update_query,
            variable_values=values,
            context=context
        )
        self.assertIsNotNone(response)

        expected_response = "{'errors': [{'message': \"You're not allowed to edit this image\", \
'locations': [{'line': 3, 'column': 13}], 'path': ['updateImage']}], 'data': {'updateImage': None}}"

        self.assertEquals(str(response), expected_response)

    def test_dont_update_any_field_mutation(self):
        """
        Located in: api_graphql => tests => test_mutations_imagemodel => TestImageModelMutations

        Image before updating:
        - title= 'images'

        Image after updating:
        - title = 'updated_image_title'
        """

        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)
        user = User.objects.latest('id')

        values = {"id": "1"}
        context = MockContext(user=user, method='POST')
        response = self.client.execute(
            self.update_query,
            variable_values=values,
            context=context
        )
        self.assertIsNotNone(response)

        expected_response = "{'data': {'updateImage': {'success': True, 'data': {'title': 'images'}}}}"

        self.assertEquals(str(response), expected_response)
