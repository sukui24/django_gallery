import graphene

from graphql.type.definition import GraphQLResolveInfo

from django.db.models import QuerySet

from taggit.models import Tag

from api_graphql.utils import get_queryset_or_error


class TagResolver:

    def resolve_all_tags(root: graphene.ObjectType, info: GraphQLResolveInfo) -> QuerySet:
        return get_queryset_or_error(Tag)
