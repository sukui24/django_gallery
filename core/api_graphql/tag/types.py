from graphene_django import DjangoObjectType

from taggit.models import Tag


class TagType(DjangoObjectType):

    class Meta:
        model = Tag
