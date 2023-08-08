from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),
    path('profile/<str:id>', views.userProfile, name='profile'),
    path('edit_user/<str:id>', views.editUser, name='edit-user'),
    path('user_images/<str:id>', views.userImages, name='user-images'),
]
