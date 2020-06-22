import pytest
from django.contrib.auth.models import User
from like_object.models import LikeObject
from user_profile.models import Profile
from tweet_object.models import TweetObject
from like_object.views import LikeObjectViewSet

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
    client.force_authenticate(testUser0)
    return client


@pytest.fixture
def testViewTest(testUser0: Profile, testUser1: Profile) -> LikeObjectViewSet:
    """
    Creates 3 Follows and returns a
    LikeObjectViewSet instance
    """
    tweet1 = TweetObject.objects.create(
        text="Test tweet 1!", author=testUser0, id="1")
    tweet2 = TweetObject.objects.create(
        text="Test tweet 2!", author=testUser1, id="2")
    like1 = LikeObject.objects.create(
        tweet=tweet1, author=testUser1
    )
    like2 = LikeObject.objects.create(
        tweet=tweet2, author=testUser0
    )
    return LikeObjectViewSet()
