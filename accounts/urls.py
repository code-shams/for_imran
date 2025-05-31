from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('pass_change/', views.pass_change, name='pass_change'),
    path('profile/upload-photo/', views.upload_profile_photo, name='upload_profile_photo'),
]
