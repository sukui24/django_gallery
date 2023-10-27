import graphene

from graphql.type.definition import GraphQLResolveInfo

from api_graphql.utils import (
    get_model_by_id_or_error,
    get_queryset_or_error
)

from django.db.models import Model, QuerySet

from base.models import ImageModel


class ImageResolver:

    def resolve_image_by_id(root: graphene.ObjectType, info: GraphQLResolveInfo, id: int) -> Model:
        return get_model_by_id_or_error(ImageModel, id)

    def resolve_all_images(root: graphene.ObjectType, info: GraphQLResolveInfo) -> QuerySet:
        return get_queryset_or_error(ImageModel)
