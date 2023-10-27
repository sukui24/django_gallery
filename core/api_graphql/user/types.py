
import graphene

from graphene_django import DjangoObjectType

from users_app.models import User


class UserType(DjangoObjectType):
    full_name = graphene.String()

    class Meta:
        model = User
        fields = '__all__'

    def resolve_full_name(parent: User, info):
        return f"{parent.first_name} {parent.last_name}"


class UserOutputType(UserType):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
