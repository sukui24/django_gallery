import graphene

from graphql.type.definition import GraphQLResolveInfo


from api_graphql.user.inputs import UserRegisterInput, UserUpdateInput
from api_graphql.user.types import UserOutputType, UserType


from api_graphql.user.services import (
    UserRegisterService,
    UserDeleteService,
    UserUpdateService
)


class UserRegisterMutation(graphene.Mutation):
    """
    User register mutation

    Send `POST` request with filling required (see `ImageModelCreateInput`) fields and send image
    with your request, you dont have to set image somewhere. Just send image with form using
    multipart/form-data

    `Permissions:`
    - Only authorized users can create images

    `Returns:`
    - success fields
    - changed model
    """
    class Arguments:
        input_ = UserRegisterInput(required=True)

    success = graphene.Boolean()
    data = graphene.Field(UserOutputType)

    def mutate(self, info: GraphQLResolveInfo, input_: UserRegisterInput):

        user = UserRegisterService.register_user(info, input_)

        return UserRegisterMutation(success=True, data=user)


class UserDeleteMutation(graphene.Mutation):
    """
    User account delete mutation.

    Send `POST` request with id delete account

    Only user itself and admins can delete accounts
    """
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info: GraphQLResolveInfo, id):

        success = UserDeleteService.delete_account(info, id)

        return UserDeleteMutation(success=success)


class UserUpdateMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        input_ = UserUpdateInput()

    success = graphene.Boolean()
    data = graphene.Field(UserType)

    def mutate(self, info: GraphQLResolveInfo, input_, id):
        """
        User update mutation

        Send `POST` and function will handle all upgrades. This
        mutation works like `PATCH` method, you're not forced to send
        all fields, you can update only few of them

        Only hosts and admins can update images
        """
        user = UserUpdateService.update_account(info, input_, id)

        return UserUpdateMutation(success=True, data=user)
