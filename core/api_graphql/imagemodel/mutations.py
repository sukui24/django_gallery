import graphene

from graphql.type.definition import GraphQLResolveInfo

from api_graphql.imagemodel.inputs import ImageModelCreateInput, ImageModelDetailnput
from api_graphql.imagemodel.types import ImageModelOutputType
from api_graphql.imagemodel.services import (
    ImageModelUploadService,
    ImageModelDeleteService,
    ImageModelUpdateService
)


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

        image = ImageModelUploadService.upload_image(info, input_)

        return ImageModelCreateMutation(success=True, data=image)


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

        success = ImageModelDeleteService.delete_image(info, id)

        return ImageModelDeleteMutation(success=success)


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

        if image := ImageModelUpdateService.update_image(info, input_, id):
            success = True
            return ImageUpdateMutation(success=success, data=image)
        else:
            success = False
            return ImageUpdateMutation(success=success, data=None)
