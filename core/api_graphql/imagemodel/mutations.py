import graphene

from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo

from base.models import ImageModel

from api_graphql.imagemodel.inputs import ImageModelCreateInput, ImageModelDetailnput
from api_graphql.imagemodel.types import ImageModelOutputType
from api_graphql.imagemodel.utils import set_unique_name


class ImageModelCreateMutation(graphene.Mutation):
    """
    Image creation (uploading) mutation

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
        input_ = ImageModelCreateInput(required=True)

    success = graphene.Boolean()
    data = graphene.Field(ImageModelOutputType)

    def mutate(self, info: GraphQLResolveInfo, input_):
        context = info.context

        if not context.user.is_authenticated:
            return GraphQLError("Only authenticated users can upload images")

        if context.method != "POST" or not context.FILES:
            return GraphQLError("Image was not provided in the POST request")

        if len(context.FILES) != 1:
            return GraphQLError("You should send only one image!")

        uploaded_image = context.FILES['0']
        title = input_.title
        description = input_.description or ''
        is_private = input_.is_private

        obj = ImageModel(
            unique_name='',
            title=title,
            description=description,
            host=context.user,
            is_private=is_private,
            image=uploaded_image
        )

        obj.save()

        return ImageModelCreateMutation(success=True, data=obj)


class ImageModelDeleteMutation(graphene.Mutation):
    """
    Image delete mutation.

    Send `POST` request with id to delete image.

    Only hosts and admins can delete images
    """
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info: GraphQLResolveInfo, id):
        context = info.context

        if context.method != "POST":
            return GraphQLError(f"Expected `POST` request, got {context.method}")

        try:
            image = ImageModel.objects.get(pk=id)

            if context.user == image.host or context.user.is_staff:
                image.delete()
                return ImageModelDeleteMutation(success=True)
            else:
                return GraphQLError("Only image host can delete it")
        except ImageModel.DoesNotExist:
            return GraphQLError(f"Image with id {id} does not exists")


class ImageUpdateMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        input_ = ImageModelDetailnput()

    success = graphene.Boolean()
    data = graphene.Field(ImageModelOutputType)

    def mutate(self, info: GraphQLResolveInfo, input_, id):
        """
        Image update mutation

        Send `POST` and function will handle all upgrades. This
        mutation works like `PATCH` method, you're not forced to send
        all fields, you can update only few of them

        Only hosts and admins can update images
        """
        context = info.context

        if context.method != "POST":
            return GraphQLError(f"Expected `POST` request, got {context.method}")

        if len(context.FILES) > 1:
            return GraphQLError("You should send only one image!")

        try:
            obj = ImageModel.objects.get(pk=id)
        except ImageModel.DoesNotExist:
            return GraphQLError(f"Image with id {id} does not exists")

        if context.user == obj.host or context.user.is_staff:
            obj.image = context.FILES['0'] if context.FILES else obj.image
            obj.title = input_.title or obj.title
            obj.description = input_.description or obj.description
            obj.is_private = input_.is_private or obj.is_private

            obj.save()
            if context.FILES:
                set_unique_name(obj)
        else:
            return GraphQLError("You're not allowed to edit this image")

        return ImageUpdateMutation(success=True, data=obj)
