from django.test import TestCase, Client
from api_graphql.schemas import schema
from graphene.test import Client as GraphQLClient
from django.urls import reverse
from .fixtures import (
    create_image,
    create_multiple_images,
    create_superuser,
    create_multiple_users)
from base.models import ImageModel
from users_app.models import User


class TestQueriesImageModel(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.endpoint_url = reverse('graphql')

    def test_graphql_execution_imagemodel_GET(self):
        """
        Located in: api_graphql => tests => test_urls => TestQueriesImageModel
        """
        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)

        query = """
        query {
            allImages {
                id
            }
        }
        """
        response = self.client.execute(query)
        self.assertIsNotNone(response)

        excpected_response = "{'data': {'allImages': [{'id': '1'}]}}"

        self.assertEquals(str(response), excpected_response)

    def test_graphql_execution_multiple_images_GET(self):
        """
        Located in: api_graphql => tests => test_urls => TestQueriesImageModel
        """
        create_multiple_images(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 3)

        query = """
        query {
            allImages{
                id
            }
        }
        """
        response = self.client.execute(query)
        self.assertIsNotNone(response)

        excpected_response = """{'data': {'allImages': [{'id': '1'}, {'id': '2'}, {'id': '3'}]}}"""

        self.assertEquals(str(response), excpected_response)

    def test_query_with_variable(self):
        """
        Located in: api_graphql => tests => test_urls => TestQueriesImageModel
        """
        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)

        query = """
        query image_by_id($id: ID){
            imageById(id: $id) {
                id
                title
            }
        }
        """
        response = self.client.execute(query, variable_values={'id': 1})
        self.assertIsNotNone(response)

        excpected_response = "{'data': {'imageById': {'id': '1', 'title': 'images'}}}"

        self.assertEquals(str(response), excpected_response)

    def test_query_with_wrong_variable(self):
        """
        Located in: api_graphql => tests => test_urls => TestQueriesImageModel
        """
        create_image(self.django_client)
        self.assertEquals(ImageModel.objects.count(), 1)

        query = """
        query image_by_id($id: ID){
            imageById(id: $id) {
                id
                title
            }
        }
        """
        response = self.client.execute(query, variable_values={'id': 2})
        self.assertIsNotNone(response)

        excpected_response = "{'errors': [{'message': 'ImageModel matching query does not exist.', \
'locations': [{'line': 3, 'column': 13}], 'path': ['imageById']}], 'data': {'imageById': None}}"

        self.assertEquals(str(response), excpected_response)


class TestQueriesUser(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.endpoint_url = reverse('graphql')

    def test_graphql_execution_user_GET(self):
        """
        Located in: api_graphql => tests => test_urls => TestQueriesUser
        """
        create_superuser(self.django_client)
        self.assertEquals(User.objects.count(), 1)

        query = """
        query {
            allUsers{
                id
            }
        }
        """
        response = self.client.execute(query)
        self.assertIsNotNone(response)

        excpected_response = "{'data': {'allUsers': [{'id': '1'}]}}"

        self.assertEquals(str(response), excpected_response)

    def test_graphql_execution_multiple_users_GET(self):
        """
        Located in: api_graphql => tests => test_urls => TestQueriesUser
        """
        create_multiple_users()
        self.assertEquals(User.objects.count(), 3)

        query = """
        query {
            allUsers{
                id
            }
        }
        """
        response = self.client.execute(query)
        self.assertIsNotNone(response)

        excpected_response = """{'data': {'allUsers': [{'id': '1'}, {'id': '2'}, {'id': '3'}]}}"""

        self.assertEquals(str(response), excpected_response)
