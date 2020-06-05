import pytest
from django.contrib.auth.models import User
from user_profile.models import Profile
from tweet_item.models import TweetItem
from retweet_object.views import RetweetObjectViewSet
from retweet_object.models import RetweetObject

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
def testViewTest(
        testUser0: Profile,
        testUser1: Profile) -> RetweetObjectViewSet:
    """
    Creates 3 Tweets and 2 Retweets and returns a
    RetweetObjectViewSet instance
    """
    tweet1 = TweetItem.objects.create(
        text="Test tweet 1!", author=testUser0, id="1")
    tweet2 = TweetItem.objects.create(
        text="Test tweet 2!", author=testUser1, id="2")
    tweet3 = TweetItem.objects.create(
        text="I am a retweet 1!", author=testUser1, id="3")
    tweet4 = TweetItem.objects.create(
        text="I am a retweet 2!", author=testUser0, id="4")
    retweet1 = RetweetObject.objects.create(
        target_tweet=tweet1, parent_tweet=tweet2
    )
    retweet2 = RetweetObject.objects.create(
        target_tweet=tweet3, parent_tweet=tweet4
    )
    return RetweetObjectViewSet()
