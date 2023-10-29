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
    if isinstance(obj, ModelBase):
        try:
            return obj.objects.get(pk=id)
        except obj.DoesNotExist:
            return GraphQLError(f"Object {obj.__name__} of id {id} does not exist")
        except Exception as e:
            return GraphQLError(f"Something went wrong: {e}")
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
    if isinstance(obj, ModelBase):
        try:
            return obj.objects.all()
        except obj.DoesNotExist:
            return GraphQLError(f"There's no available records in {obj.__name__}")
        except Exception as e:
            return GraphQLError(f"Something went wrong: {e}")
    else:
        message = f"{obj} should be a Model, got '{type(obj).__name__}' instead"
        return GraphQLError(message)
