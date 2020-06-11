import pytest
from django.contrib.auth.models import User
from tweet_item.models import TweetItem
from tweet_item.views import TweetItemViewSet
from user_profile.models import Profile

pytestmark = pytest.mark.django_db


@pytest.fixture
def testUser() -> Profile:
    """
    Generate a user
    """
    user = User.objects.create_user(
        username="testUser",
        email="admin@email.com",
        password="testPassword123")
    profile = Profile.objects.create(
        user=user,
        display_name="testUser name"
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
        password="testPassword123")
    profile = Profile.objects.create(
        user=user,
        display_name="testUser1 name"
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
    Generate a rest_frameworks APICLient
    """
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture
def testViewTest(testUser: Profile, testUser1: Profile) -> TweetItemViewSet:
    """
    Creates 3 TweetItems (2 by testUser and 1 by testUser1) and returns a
    TweetItemViewSet instance
    """
    tweet1 = TweetItem.objects.create(
        text="Test tweet 1!", author=testUser, id="1")
    tweet2 = TweetItem.objects.create(
        text="Test tweet 2!", author=testUser, id="2")
    tweet3 = TweetItem.objects.create(
        text="Test tweet 3!", author=testUser1, id="3")
    tweet4 = TweetItem.objects.create(
        text="I am a retweet 1!",
        author=testUser, id="4", retweet=tweet3)
    tweet5 = TweetItem.objects.create(
        text="I am a comment 1!",
        author=testUser1, id="5", comment=tweet2)
    tweet6 = TweetItem.objects.create(
        text="I am a comment 2!",
        author=testUser1, id="6", comment=tweet5)
    return TweetItemViewSet()
