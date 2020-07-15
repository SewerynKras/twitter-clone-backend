from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from user_profile import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.ProfileViewSet)

urlpatterns = [
    path("getMyProfile/", views.MyProfileView.as_view()),    
    path("", include(router.urls))
]
