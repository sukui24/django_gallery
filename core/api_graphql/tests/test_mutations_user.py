from users_app.models import User
from django.test import TestCase, Client
from api_graphql.schemas import schema
from graphene.test import Client as GraphQLClient
from .fixtures import MockContext, create_defaultuser, create_multiple_users


class TestRegisterUserMutation(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.context = MockContext(method='POST')
        self.query = """
        mutation (
            $firstName:String!,
            $username:String!,
            $email:String!,
            $password:String!,
            $password2:String!
            ) {
            registerUser(
                input_: {firstName: $firstName,
                username: $username,
                email: $email,
                password: $password,
                password2: $password2}
            ) {
                data {
                fullName
                email
                username
                }
                success
            }
        }
        """

    def test_register_user_mutation(self) -> None:
        """
        Located in: api_graphql => tests => test_mutations_user => TestRegisterUserMutation
        """
        response = self.client.execute(self.query, variable_values={
            "firstName": "TestUser",
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "testuser1234",
            "password2": "testuser1234"
        }, context=self.context)

        self.assertIsNotNone(response)
        self.assertEquals(User.objects.count(), 1)

        expected_response = "{'data': {'registerUser': {'data': {'fullName': 'TestUser ', \
'email': 'testuser@gmail.com', 'username': 'testuser'}, 'success': True}}}"

        self.assertEquals(str(response), expected_response)

    def test_register_user_wrong_password_mutation(self) -> None:
        """
        Located in: api_graphql => tests => test_mutations_user => TestRegisterUserMutation
        """
        response = self.client.execute(self.query, variable_values={
            "firstName": "TestUser",
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "somepassword",
            "password2": "somewrongpassword"
        }, context=self.context)

        self.assertIsNotNone(response)
        self.assertEquals(User.objects.count(), 0)

        expected_response = "{'errors': [{'message': \"Passwords didn't match, try again\", \
'locations': [{'line': 9, 'column': 13}], 'path': ['registerUser']}], 'data': {'registerUser': None}}"

        self.assertEquals(str(response), expected_response)


class TestDeleteUserMutation(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.query = """
        mutation ($id:ID) {
            deleteUser(id: $id) {
                success
            }
        }
        """

    def test_account_delete_mutation(self) -> None:
        """
        Located in: api_graphql => tests => test_mutations_user => TestDeleteUserMutation
        """
        create_defaultuser(self.django_client)
        self.assertEquals(User.objects.count(), 1)
        user = User.objects.get(pk=1)
        context = MockContext(user=user, method='POST')

        response = self.client.execute(self.query, variable_values={
            "id": 1
        }, context=context)
        self.assertIsNotNone(response)
        self.assertEquals(User.objects.count(), 0)

        expected_response = "{'data': {'deleteUser': {'success': True}}}"

        self.assertEquals(str(response), expected_response)

    def test_account_delete_wrong_id_mutation(self) -> None:
        """
        Located in: api_graphql => tests => test_mutations_user => TestDeleteUserMutation
        """
        create_multiple_users()
        self.assertEquals(User.objects.count(), 3)
        user = User.objects.get(pk=3)
        context = MockContext(user=user, method='POST')

        response = self.client.execute(self.query, variable_values={
            "id": 1
        }, context=context)
        self.assertIsNotNone(response)
        self.assertEquals(User.objects.count(), 3)

        expected_response = "{'errors': [{'message': 'Only user itself or admins can delete account', \
'locations': [{'line': 3, 'column': 13}], 'path': ['deleteUser']}], 'data': {'deleteUser': None}}"

        self.assertEquals(str(response), expected_response)


class TestUpdateUserMutation(TestCase):

    def setUp(self):
        self.client = GraphQLClient(schema)
        self.django_client = Client()
        self.query = """
        mutation ($id: ID, $firstName: String) {
            updateUser(id: $id, input_: {firstName: $firstName}) {
                data {
                firstName
                }
                success
            }
        }
        """

    def test_update_user_mutation(self) -> None:
        """
        Located in: api_graphql => tests => test_mutations_user => TestUpdateUserMutation

        first_name = "testuser"
        """
        create_defaultuser(self.django_client)
        self.assertEquals(User.objects.count(), 1)
        user = User.objects.get(pk=1)
        context = MockContext(user=user, method='POST')

        response = self.client.execute(self.query, variable_values={
            "id": 1,
            "firstName": "edited_testuser"
        }, context=context)
        self.assertIsNotNone(response)

        expected_response = "{'data': {'updateUser': {'data': {'firstName': 'edited_testuser'}, 'success': True}}}"

        self.assertEquals(str(response), expected_response)

    def test_update_wrong_user_mutation(self) -> None:
        """
        Located in: api_graphql => tests => test_mutations_user => TestUpdateUserMutation
        """
        create_multiple_users()
        self.assertEquals(User.objects.count(), 3)
        user = User.objects.get(pk=3)
        context = MockContext(user=user, method='POST')

        response = self.client.execute(self.query, variable_values={
            "id": 1,
            "firstName": "edited_testuser"
        }, context=context)
        self.assertIsNotNone(response)

        expected_response = "{'errors': [{'message': 'Only user itself or admins can update account', \
'locations': [{'line': 3, 'column': 13}], 'path': ['updateUser']}], 'data': {'updateUser': None}}"

        self.assertEquals(str(response), expected_response)
