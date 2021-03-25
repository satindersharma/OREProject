from django.contrib import admin
from django.urls import path, include
from .views import (SignUpView, UserLoginView, UserLogoutView, CustomPasswordResetView,UserProfileView, 
DeleteProfileImage, Home, GetOREUserView,GetOREAppTokenView,CreateOREUserView)
app_name = 'users'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('get-user/', GetOREUserView.as_view(), name='ore-user'),
    path('create-ore-user/', CreateOREUserView.as_view(), name='create-ore-user'),
    path('get-ore-token/', GetOREAppTokenView.as_view(), name='ore-token'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('delete-image/', DeleteProfileImage.as_view(), name='delete-image'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    
]