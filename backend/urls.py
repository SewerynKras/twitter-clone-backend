from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweet_item.urls')),
    path('users/', include('user_profile.urls')),
    path('follow/', include('follow_object.urls'))
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
