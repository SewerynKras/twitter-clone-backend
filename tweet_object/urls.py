from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from tweet_object import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TweetObjectViewSet)

urlpatterns = [
    path('', include(router.urls))
]
