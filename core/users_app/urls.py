from django.urls import path
from users_app import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.login_user, name='login'),
    path('profile/<str:id>', views.user_profile, name='profile'),
    path('edit_user/<str:id>', views.edit_user, name='edit-user'),
    path('user_images/<str:id>', views.user_images, name='user-images'),
    path('user_images/<str:id>/private',
         views.user_images_private, name='user-images-private'),
    path('delete_account/<str:id>', views.delete_accout, name='delete-account'),
]
