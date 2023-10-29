from graphql import GraphQLError
from base.models import ImageModel
from api_graphql.imagemodel.inputs import ImageModelCreateInput
from graphql.type.definition import GraphQLResolveInfo


class ImageModelUploadService:
    """
    Class has only one method - `upload_image(input_, info)`. This method
    takes user `input` and graphql request `info` and after some validation
    create and return instance of `ImageModel`
    """
    @classmethod
    def upload_image(cls, info: GraphQLResolveInfo, input_: ImageModelCreateInput) -> ImageModel:
        """
        Input:
        - `info` - `GraphQLResolveInfo` instance obj. Usually it's automatically
                    collect all needed data and transfer it as `info` object, but it's also mutable
        - `input_` - Image input from mutation. Should match the `ImageModelCreateInput` fields

        Output:
        - created `ImageModel` instance

        Permissions: Authenticated users only
        """
        context = info.context

        if cls._validate_request(context):
            return cls._create_image(input_, context)

    @staticmethod
    def _validate_request(context) -> bool:

        if not context.user.is_authenticated:
            raise GraphQLError("Only authenticated users can upload images")

        if context.method != "POST" or not context.FILES:
            raise GraphQLError("Image was not provided in the POST request")

        if len(context.FILES) > 1:
            raise GraphQLError("You should send only one image!")

        return True

    @classmethod
    def _create_image(cls, input_: ImageModelCreateInput, context) -> ImageModel:

        uploaded_image = context.FILES['0']

        image_data = {
            "unique_name": '',
            "title": input_.title,
            "description": input_.description or '',
            "host": context.user,
            "is_private": input_.is_private,
            "image": uploaded_image,
        }

        image = ImageModel(**image_data)
        image.save()
        return image


class ImageModelDeleteService:
    """
    Class has only one method - `delete_image(input_, info)`. This method
    takes user `input` and graphql request `info` and after some validation
    deletes an image
    """
    @classmethod
    def delete_image(cls, info: GraphQLResolveInfo, id: int) -> bool:
        """
        Input:
        - `info` - `GraphQLResolveInfo` instance obj. Usually it's automatically
                    collect all needed data and transfer it as `info` object, but it's also mutable
        - `id` - ID of image that should be deleted

        Output:
        - Boolean, indicates if image is deleted (`True`) or not (`False`)

        Permissions: Only host of image or admins can delete image
        """
        context = info.context

        if cls._validate_request(context):
            image = cls._get_image_or_error(context, id)
            image.delete()
            if cls._check_image_deletion(id):
                return True

        return False

    @staticmethod
    def _validate_request(context) -> bool:

        if not context.user.is_authenticated:
            raise GraphQLError("Only authenticated users can delete images")

        if context.method != "POST":
            raise GraphQLError(
                f"Expected `POST` request, got {context.method}")

        return True

    @staticmethod
    def _get_image_or_error(context, id) -> ImageModel:
        """
        Return ImageModel instance if request made by host of image or by admin

        Otherwise raises GraphQLError
        """
        try:
            image = ImageModel.objects.get(pk=id)
            if context.user == image.host or context.user.is_staff:
                return image
            else:
                raise GraphQLError("Only image host can delete it")
        except ImageModel.DoesNotExist:
            raise GraphQLError(f"Image with id {id} does not exists")

    @staticmethod
    def _check_image_deletion(id):
        try:
            ImageModel.objects.get(pk=id)
        except ImageModel.DoesNotExist:
            return True
        else:
            return False


class ImageModelUpdateService:

    @classmethod
    def update_image(cls,
                     info: GraphQLResolveInfo,
                     input_: ImageModelCreateInput,
                     id: int) -> ImageModel:
        """
        Function to update image. It works like `PATCH` request, can update
        only one of fields, or every field.

        Input:
        - `info` - `GraphQLResolveInfo` instance obj. Usually it's automatically
                    collect all needed data and transfer it as `info` object, but it's also mutable
        - `input_` - Input data that should be changed on
        - `id` - ID of image that should be deleted

        Output:
        - Updated `ImageModel` instance

        Permissions: Only image host or admins can update image
        """

        context = info.context

        cls._validate_request(context)
        image_instance = cls._get_image_or_error(context, id)
        image_updated = cls._apply_image_updates(
            context, input_, image_instance)
        return image_updated

    @staticmethod
    def _validate_request(context) -> bool:

        if not context.user.is_authenticated:
            raise GraphQLError("Only authenticated users can edit images")

        if context.method != "POST":
            raise GraphQLError(
                f"Expected `POST` request, got {context.method}")

        if len(context.FILES) > 1:
            raise GraphQLError("You should send only one image!")

        return True

    @staticmethod
    def _get_image_or_error(context, id: str) -> ImageModel:
        """
        Return image instance if request made by image host or by admin

        Otherwise raises GraphQLError
        """
        try:
            image = ImageModel.objects.get(pk=id)
            if context.user == image.host or context.user.is_staff:
                return image
            else:
                raise GraphQLError(
                    "You're not allowed to edit this image")
        except ImageModel.DoesNotExist:
            raise GraphQLError(f"Image with id {id} does not exists")

    @staticmethod
    def _apply_image_updates(context,
                             input_: ImageModelCreateInput,
                             image: ImageModel) -> ImageModel:

        # None means actual image file wouldn't be updated
        image_file = context.FILES['0'] if context.FILES else None

        attributes_to_update = {
            "title": input_.title,
            "description": input_.description,
            "is_private": input_.is_private,
            "image": image_file,
        }

        for attribute, value in attributes_to_update.items():
            if value is not None:
                setattr(image, attribute, value)

        image.save()

        return image
