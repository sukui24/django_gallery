from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),


    path('', views.home, name='home'),
    path('add_image/', views.addImage, name='add-image'),
    path('view_image/<str:unique_name>', views.viewImage, name='view-image'),
    path('delete_image/<str:unique_name>',
         views.deleteImage, name='delete-image'),
]
