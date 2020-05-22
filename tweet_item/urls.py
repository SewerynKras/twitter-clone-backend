from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from tweet_item import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TweetItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
