from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path, include

from .views import (
    ImageViewSet,
    UserViewSet,
)


router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='imagemodel')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    # customized View by new serializer
    path('login/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
