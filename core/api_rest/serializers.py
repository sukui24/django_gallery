from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from taggit.serializers import (
    TagListSerializerField,
    TaggitSerializer
)

from users_app.models import User
from base.models import ImageModel

from rest_framework.serializers import (
    HyperlinkedRelatedField,
    HyperlinkedIdentityField
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Overrided Token Serializer to make more fields encoded in Token
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer provides `list` and `retrieve` actions with only
    public fields that allowed for default users

    All fields would be allowed for admins only
    """
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_staff',
                   'is_active', 'date_joined', 'groups',
                   'user_permissions']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer provide `create` action for User model
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'bio', 'avatar', 'phone_number',
                  'country', 'city', 'adress', 'password']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer provides all actions, except `create`,
    related to User model
    """
    user_indentity_url = HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = '__all__'


class ListImageSerializer(serializers.ModelSerializer):
    """
    Serializer provides `list` action with only fields that
    needed on album component
    """
    image_indentity_url = HyperlinkedIdentityField('imagemodel-detail')
    host = HyperlinkedRelatedField(
        view_name='imagemodel-detail', read_only=True)

    tags = TagListSerializerField(required=False)

    class Meta:
        model = ImageModel
        exclude = ['unique_name', 'updated_at', 'created_at']


class ViewImageSerializer(TaggitSerializer,
                          serializers.ModelSerializer):
    """
    Serializer provides `retrieve` action with fields
    needed in view image page
    """
    image_indentity_url = HyperlinkedIdentityField('imagemodel-detail')
    host = HyperlinkedRelatedField(
        view_name='imagemodel-detail', read_only=True)

    # Using ReadOnlyField for 'host' to prevent modification.
    tags = TagListSerializerField(required=False)

    class Meta:
        model = ImageModel
        exclude = ['unique_name']


class DetailImageSerializer(TaggitSerializer,
                            serializers.HyperlinkedModelSerializer):
    """
    Serializer provides `destroy`, `create` and `update` actions
    with all fields
    """
    tags = TagListSerializerField(required=False)

    class Meta:
        model = ImageModel
        fields = '__all__'
