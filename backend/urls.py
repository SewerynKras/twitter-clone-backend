from django.contrib import admin
from django.urls import path, include
# from backend.tweet_item import views
# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'tweets', views.TweetItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweet_item.urls')),
    path('users/', include('user_profile.urls'))
    # path('', include(router.urls)),
    # path('api-url/', include('rest_framework.urls', namespace='rest_framework'))
]
