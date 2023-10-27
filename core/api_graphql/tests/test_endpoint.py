from django.test import TestCase
from django.urls import reverse, resolve
from graphene_file_upload.django import FileUploadGraphQLView
from api_graphql.schemas import schema
from graphene.test import Client as GraphQLClient


class TetsGraphQLEndpoint(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.endpoint_url = reverse('graphql')

    def test_graphql_endpoint_is_resolved(self):
        """
        Located in: api_graphql => tests => test_endpoint => TetsGraphQLEndpoint
        """
        response = self.client.execute("""
        query {
            allImages{
                id
            }
        }
        """)
        self.assertIsNotNone(response)
        excpected_response = "{'data': {'allImages': []}}"

        self.assertEquals(str(response), excpected_response)
        self.assertEquals(
            resolve(self.endpoint_url).func.view_class, FileUploadGraphQLView)
