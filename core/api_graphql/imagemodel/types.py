import graphene

from graphene_django import DjangoObjectType

from base.models import ImageModel

from api_graphql.tag.types import TagType


class ImageModelType(DjangoObjectType):
    images_tags = graphene.List(TagType)

    class Meta:
        model = ImageModel
        exclude = ['tags']

    def resolve_image_tags(image: ImageModel, info):
        return image.tags.all()


class ImageModelOutputType(DjangoObjectType):
    image_tags = graphene.List(TagType)

    class Meta:
        model = ImageModel
        exclude = ['tags', 'created_at', 'updated_at',
                   'host', 'image_views']

    def resolve_image_tags(image: ImageModel, info):
        return image.tags.all()
