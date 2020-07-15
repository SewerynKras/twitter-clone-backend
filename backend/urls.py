from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path(
        'token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'tweets/',
        include('tweet_object.urls')),
    path(
        'users/',
        include('user_profile.urls')),
    path(
        'follow/',
        include('follow_object.urls')),
    path(
        'likes/',
        include('like_object.urls')),
]
