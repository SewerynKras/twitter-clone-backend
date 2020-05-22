from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from user_profile import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls))
]
