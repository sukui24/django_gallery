import graphene


class ImageModelDetailnput(graphene.InputObjectType):
    """
    Inputs for create and update actions

    `image` didnt required cause you can't send files directly in graphql request.
    """
    image = graphene.String()
    title = graphene.String()
    is_private = graphene.Boolean()
    image_tags = graphene.String()
    description = graphene.String()


class ImageModelCreateInput(ImageModelDetailnput):
    """
    Inheirts from `ImageModelDetailnput` but `title` and `is_private` are required

    `image` didnt required cause you can't send files directly in graphql request.
    """
    title = graphene.String(required=True)
    is_private = graphene.Boolean(required=True)
