import graphene

from graphql.type.definition import GraphQLResolveInfo

from graphene_django.debug import DjangoDebug

from api_graphql.imagemodel.types import ImageModelType
from api_graphql.user.types import UserType
from api_graphql.tag.types import TagType

from api_graphql.imagemodel.resolvers import ImageResolver
from api_graphql.user.resolvers import UserResolver
from api_graphql.tag.resolvers import TagResolver

from api_graphql.imagemodel.mutations import (
    ImageModelCreateMutation,
    ImageModelDeleteMutation,
    ImageUpdateMutation
)
from api_graphql.user.mutations import (
    UserRegisterMutation,
    UserDeleteMutation,
    UserUpdateMutation
)


class Query(graphene.ObjectType):

    all_images = graphene.List(ImageModelType)
    image_by_id = graphene.Field(ImageModelType, id=graphene.ID())
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID())
    all_tags = graphene.List(TagType)
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_image_by_id(root: 'Query', info: GraphQLResolveInfo, id: int):
        return ImageResolver.resolve_image_by_id(root, info, id)

    def resolve_all_images(root: 'Query', info: GraphQLResolveInfo):
        return ImageResolver.resolve_all_images(root, info)

    def resolve_user_by_id(root: 'Query', info: GraphQLResolveInfo, id: int):
        return UserResolver.resolve_user_by_id(root, info, id)

    def resolve_all_users(root: 'Query', info: GraphQLResolveInfo):
        return UserResolver.resolve_all_users(root, info)

    def resolve_all_tags(root: 'Query', info: GraphQLResolveInfo):
        return TagResolver.resolve_all_tags(root, info)


class Mutation(graphene.ObjectType):
    create_image = ImageModelCreateMutation.Field()
    delete_image = ImageModelDeleteMutation.Field()
    update_image = ImageUpdateMutation.Field()
    register_user = UserRegisterMutation.Field()
    delete_user = UserDeleteMutation.Field()
    update_user = UserUpdateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
