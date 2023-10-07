from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from taggit.serializers import (
    TagListSerializerField,
    TaggitSerializer
)

from users_app.models import User
from base.models import ImageModel


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

    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True}}


class ListImageSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer provides `list` action with only fields that
    needed on album component
    """
    tags = TagListSerializerField(required=False)

    class Meta:
        model = ImageModel
        exclude = ['unique_name', 'updated_at', 'created_at']

    def to_representation(self, instance):
        """
        Override the to_representation method to change the URL format.
        """
        ret = super().to_representation(instance)
        ret['url'] = self.context['request'].build_absolute_uri(
            f'/api/images/{instance.id}/')
        return ret


class ViewImageSerializer(TaggitSerializer,
                          serializers.HyperlinkedModelSerializer):
    """
    Serializer provides `retrieve` action with fields
    needed in view image page
    """
    # Using ReadOnlyField for 'host' to prevent modification.
    tags = TagListSerializerField(required=False)

    class Meta:
        model = ImageModel
        exclude = ['url', 'unique_name']

    def to_representation(self, instance):
        """
        Override the to_representation method to change the URL format.
        """
        ret = super().to_representation(instance)
        ret['url'] = self.context['request'].build_absolute_uri(
            f'/api/images/{instance.id}/')
        return ret


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
