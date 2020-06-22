from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweet_object.urls')),
    path('users/', include('user_profile.urls')),
    path('follow/', include('follow_object.urls')),
    path('likes/', include('like_object.urls')),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
