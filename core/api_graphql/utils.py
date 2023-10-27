from typing import Union

from graphql import GraphQLError

from django.db.models.base import ModelBase
from django.db.models import Model, QuerySet


def get_model_by_id_or_error(obj: ModelBase, id: id) -> Union[Model, GraphQLError]:
    """
    - Function for retrieving a model by ID or returning an error

    Input: `Model`

    Return: `Model` or `GraphQLError` if something goes wrong

    - in type hinting set `ModelBase` because all `Model` instances
    are of the `ModelBase` meta class
    """
    # ! TODO: Filter sql request for getting user provided fields
    if isinstance(obj, ModelBase):
        return obj.objects.get(pk=id)
    else:
        message = f"{obj} should be a Model, got '{type(obj).__name__}' instead"
        return GraphQLError(message)


def get_queryset_or_error(obj: ModelBase) -> Union[QuerySet, GraphQLError]:
    """
    - Function for retrieving all objects of a model or returning an error

    Input: `Model`

    Return: `QuerySet` or `GraphQLError` if something goes wrong

    - in type hinting set `ModelBase` because all `Model` instances
    are of the `ModelBase` meta class
    """
    try:
        objects = obj.objects.all()
    except Exception as e:
        return GraphQLError(f"Something went wrong: {e}")
    else:
        return objects
