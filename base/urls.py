from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('image_edit/', views.imageEdit, name='edit_image'),
    path('image_view/', views.imagePage, name='view_image'),
    path('image_add/', views.imageAdd, name='add_image'),
]
