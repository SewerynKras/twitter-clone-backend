import pytest
from django.contrib.auth.models import User
from user_profile.models import Profile
from user_profile.views import ProfileViewSet

pytestmark = pytest.mark.django_db


@pytest.fixture
def testUser() -> Profile:
    """
    Generate a user
    """
    user = User.objects.create_user(
        username="testUser",
        email="admin@email.com",
        password="testPassword123",
        id=1)
    profile = Profile.objects.create(
        user=user,
        display_name="testUser name",
        id=1
    )
    return profile


@pytest.fixture
def testUser1() -> Profile:
    """
    Generate a user
    """
    user = User.objects.create_user(
        username="testUser1",
        email="admin@email123.com",
        password="testPassword123",
        id=2)
    profile = Profile.objects.create(
        user=user,
        display_name="testUser1 name",
        id=2
    )
    return profile


@pytest.fixture
def APIClient(testUser):
    """
    Generate a rest_frameworks APICLient and authenticates it
    with testUser
    """
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(testUser)
    return client


@pytest.fixture
def APIClient_no_auth():
    """
    Generate a rest_frameworks APICLient but doesn't authenticate it
    """
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture
def testViewTest(testUser: Profile, testUser1: Profile) -> ProfileViewSet:
    """
    Creates 2 Profiles and returns a
    ProfileViewSet instance
    """
    return ProfileViewSet()
