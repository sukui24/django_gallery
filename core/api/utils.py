from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status

from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpRequest

from typing import Union


def get_all_fields(request: HttpRequest,
                   obj: Union[Model, QuerySet],
                   serializer: ModelSerializer) -> Response:
    """
    Function to provide easier procedure to get all fields
    From Model (if single object) or QuerySet.


    :param request: Just `request`
    :param obj: It should be either `Model` or `QuerySet` object
    :param serializer: Be sure you use here serializer that related
    to your Model/QuerySet
    """
    obj_error = "The 'obj' parameter should be either a Model or a QuerySet, not %s"
    serializer_error = "The 'serializer' shoud be ModelSerializer object, not %s"

    if not issubclass(serializer, ModelSerializer):
        return Response({"detail": serializer_error % type(serializer).__name__})

    context = {}
    if isinstance(obj, Model):
        many = False
    elif isinstance(obj, QuerySet):
        many = True
        # count objects in QuerySet
        context["count"] = obj.count()
    else:
        return Response({
            "detail": obj_error % f"'{type(obj).__name__}'"
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = serializer(obj, many=many, context={"request": request})
    context["result"] = serializer.data

    return Response(context, status=status.HTTP_200_OK)
