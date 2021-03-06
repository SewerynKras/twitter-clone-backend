from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from follow_object import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.FollowObjectViewSet)

urlpatterns = [
    path("getRecommendations/", views.RecommendationsView.as_view({'get': 'list'})),
    path("", include(router.urls))
]
