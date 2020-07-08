import pytest
from django.contrib.auth.models import User
from follow_object.views import FollowObjectViewSet
from follow_object.models import FollowObject
from user_profile.models import Profile

pytestmark = pytest.mark.django_db


@pytest.fixture
def testUser0() -> Profile:
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
        id=2)

    return profile


@pytest.fixture
def testUser2() -> Profile:
    """
    Generate a user
    """
    user = User.objects.create_user(
        username="testUser2",
        email="admin@email123.com",
        password="testPassword123",
        id=3)
    profile = Profile.objects.create(
        user=user,
        display_name="testUser2 name",
        id=3)

    return profile


@pytest.fixture
def APIClient_no_auth():
    """
    Generate a rest_frameworks APICLient and authenticates it
    with testUser
    """
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture
def APIClient(testUser0):
    """
    Generate a rest_frameworks APICLient and authenticates it
    with testUser
    """
    from rest_framework.test import APIClient
    client = APIClient()
    data = {"username": "testUser", "password": "testPassword123"}
    resp = client.post("/token/", data=data, follow=True)
    token = resp.data["access"]
    client.force_authenticate(token=token)
    return client


@pytest.fixture
def testViewTest(testUser0: Profile, testUser1: Profile,
                 testUser2: Profile) -> FollowObjectViewSet:
    """
    Creates 3 Follows and returns a
    FollowObjectViewSet instance

    testUser0 -> following: 1, followers: 1
    testUser1 -> following: 1, followers: 2
    testUser2 -> following: 2, followers: 1
    """
    follow0 = FollowObject.objects.create(
        following=testUser0, being_followed=testUser1)
    follow1 = FollowObject.objects.create(
        following=testUser2, being_followed=testUser0)
    follow2 = FollowObject.objects.create(
        following=testUser1, being_followed=testUser2)
    follow3 = FollowObject.objects.create(
        following=testUser2, being_followed=testUser1)
    return FollowObjectViewSet()
