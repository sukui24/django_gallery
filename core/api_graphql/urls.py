from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from api_graphql.schemas import schema

from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    path("", csrf_exempt(FileUploadGraphQLView.as_view(
        graphiql=True,
        schema=schema
    )), name="graphql")
]
