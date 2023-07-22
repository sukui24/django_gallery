from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('image_edit/', views.imageEdit, name='image_edit'),
    path('image_view/', views.imagePage, name='view_image'),
    path('image_add/', views.imageAdd, name='add_image'),
]
