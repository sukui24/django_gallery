import graphene

from graphql.type.definition import GraphQLResolveInfo

from django.db.models import Model, QuerySet

from base.models import User

from api_graphql.utils import (
    get_model_by_id_or_error,
    get_queryset_or_error
)


class UserResolver:

    def resolve_user_by_id(root: graphene.ObjectType, info: GraphQLResolveInfo, id: int) -> Model:
        return get_model_by_id_or_error(User, id)

    def resolve_all_users(root: graphene.ObjectType, info: GraphQLResolveInfo) -> QuerySet:
        return get_queryset_or_error(User)
