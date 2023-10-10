from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import (
    action
)
from rest_framework import (
    permissions,
    viewsets,
    status,
)

from django.contrib.auth import login
from django.db.models import Q


from users_app.models import User
from base.models import ImageModel
from .permissions import IsHostOrAdminOrReadOnly, IsUserOrAdmin
from .utils import get_all_fields
from .serializers import (
    ViewImageSerializer,
    UserSerializer,
    UserCreateSerializer,
    ListImageSerializer,
    DetailImageSerializer,
    PublicUserSerializer

)


class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides all actions
    related to Image Model
    """
    queryset = ImageModel.objects.all()
    serializer_class = ListImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    SAFE_ACTIONS = ['list', 'retrieve', 'create']
    PRIVATE_ACTIONS = ['update', 'destroy', 'partial_update']

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get_queryset(self):
        """
        Overriding get_queryset for search/sort purposes
        """
        # local variable used for filtering images depending
        # on who's asking the data (admin get private images as well)
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_private=False)

        q = self.request.query_params.get('q', '')
        _order = self._get_ordering(self.request)

        queryset = queryset.filter(
            Q(title__icontains=q) | Q(
                description__icontains=q) | Q(tags__name__icontains=q),
        ).order_by(_order).distinct()

        return queryset

    @action(detail=False, methods=['GET'], url_path='get_all_fields/(?P<pk>[^/.]+)')
    def get_all_fields_retrieve(self, request, pk):
        """
        Function that allows you to get all field from one image

        URL example: your_domain.com/api/images/get_all_fields/<id>

        `detail` set to false to avoid link issues like this:
            your_domain.com/images/<pk>/get_all_fields/<pk>

        **Has permissions:** Authenticated only
        """
        instance = self.get_object()
        response = get_all_fields(request, instance, DetailImageSerializer)
        return response

    @action(detail=False, methods=['GET'], url_path='get_all_fields')
    def get_all_fields_list(self, request):
        """
        Function that allows you to get every field for every image

        URL example: your_domain.com/api/images/get_all_fields

        **Has permissions:** Authenticated only
        """
        queryset = self.get_queryset()
        response = get_all_fields(request, queryset, DetailImageSerializer)
        return response

    def get_serializer_class(self):
        """
        Method returns serializer based on action

        ViewImageSerializer - returns only few fields
        DetailImageSerializer - returns all fields
        """
        if self.action == 'retrieve':
            return ViewImageSerializer
        elif self.action in self.PRIVATE_ACTIONS:
            return DetailImageSerializer
        return self.serializer_class

    def get_permissions(self):
        """
        Method returns permission based on user role
        """
        if self.action in self.SAFE_ACTIONS:
            return [permissions.IsAuthenticated()]
        elif self.action in self.PRIVATE_ACTIONS:
            return [IsHostOrAdminOrReadOnly()]
        return []

    @staticmethod
    def _get_ordering(request):
        """
        Method to sort images

        Since it's specific for images model we made it as staticmethod
        """
        sort = request.query_params.get('sort', 'most_popular')

        ORDER_OPTIONS_MAP = {
            'most_recent': '-created_at',
            'least_recent': 'created_at',
            'least_popular': 'image_views',
            'most_popular': '-image_views',
            'last_updated': '-updated_at',
        }

        ordering = ORDER_OPTIONS_MAP.get(sort, '-image_views')
        return ordering

    def create(self, request, *args, **kwargs):
        """
        POST method to create new image

        Required fields: `title`, `image`

        Host sets automatically based on whos request it is.
        > for some reason swagger didn't display image field

        **Has permissions:** Authenticated only
        """
        return super().create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        GET method to retrieve image

        Same as `list` method have few permission checkers

        **Has permissions:** Authenticated only
        """
        return super().retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        PUT method to update image

        PUT method required all fields to get successful update

        same as POST method don't have image field for some reason

        **Has permissions:** Image host, admin
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH method to update image

        PATCH method required atleast one field to get successful update

        same as POST method don't have image field for some reason

        **Has permissions:** Image host, admin
        """
        return super().update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE method to delete image

        Have few permission checkers.

        **Has permissions:** Image host, admin
        """
        return super().destroy(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        GET method to list images

        Based on user permissions return specific answer:
        > For default user - few public fields
        > For admin - all fields and private images

        Action permission handles according to this lists:

        `SAFE_ACTIONS` = ['list', 'retrieve', 'create'] - Authenticated only
        `PRIVATE_ACTIONS` = ['update', 'destroy', 'partial_update'] -\
        Host or admin or read only

        Private actions allowed only for host and admins

        **Has permissions:** Authenticated only
        """
        return super().list(self, request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides all actions
    that related to User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    SAFE_ACTIONS = ['list', 'retrieve']
    PRIVATE_ACTIONS = ['update', 'destroy', 'partial_update']

    # * For login just use login/ endpoint which will return tokens

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        POST Method provides custom register

        Here we hash users password and make jwt token for them

        Response for this is access token, refresh toke and user info

        **Has permissions:** Any
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # After saving we set hashed password to user
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            # Set token for new user
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            context = {
                "refresh": str(refresh_token),
                "access": str(access_token),
                "user": serializer.data
            },
            login(request, user)
            return Response(context, status=status.HTTP_201_CREATED)

        return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Method returns permission based on user role
        """
        if self.action in self.SAFE_ACTIONS:
            return [permissions.IsAuthenticated()]
        elif self.action in self.PRIVATE_ACTIONS:
            return [IsUserOrAdmin()]
        elif self.action == 'create':
            return [permissions.AllowAny()]
        return []

    def get_serializer_class(self):
        """
        Method returns serializer based on action

        UserCreateSerializer - returns fields for registration page
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['retrieve', 'list']:
            serializer_class = self._permission_serializer_checker(
                self.request)
            return serializer_class
        return self.serializer_class

    @staticmethod
    def _permission_serializer_checker(request):
        """
        Method returns serializer based on user role

        UserSerializer - returns all fields
        PublicUserSerializer - returns few fields
        """
        if request.user.is_superuser:
            return UserSerializer
        else:
            return PublicUserSerializer

    def create(self, request, *args, **kwargs):
        """
        POST method to create new user

        Required fields: `first_name`, `username`, `email`, `password`

        **Has permissions:** Any
        """
        return super().create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        GET method to retrieve user

        Same as `list` method have few permission checkers

        Also didn't allow non-admin users see too much info

        **Has permissions:** Authenticated only
        """
        return super().retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        PUT method to update user

        PUT method required all fields to get successful update

        **Has permissions:** User, admin
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH method to update image

        PATCH method required atleast one field to get successful update

        **Has permissions:** User, admin
        """
        return super().update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE method to delete image

        Have few permission checkers.

        **Has permissions:** User, admin
        """
        return super().destroy(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        GET method to list users

        Based on user permissions return specific answer:
        > For default user - few public fields
        > For admin - all fields

        Action permission handles according to this pattern:

        `create` - Any
        `SAFE_ACTIONS` = ['list', 'retrieve'] - Authenticated only
        `PRIVATE_ACTIONS` = ['update', 'destroy', 'partial_update'] - User or admin

        Private actions allowed only for admins

        **Has permissions:** Authenticated only
        """
        return super().list(self, request, *args, **kwargs)
