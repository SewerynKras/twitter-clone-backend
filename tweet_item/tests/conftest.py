import pytest
from django.contrib.auth.models import User
from tweet_item.models import TweetItem
from tweet_item.views import TweetItemViewSet

pytestmark = pytest.mark.django_db


@pytest.fixture
def testUser() -> User:
    """
    Generate a user
    """
    return User.objects.create_user(
        username="testUser",
        email="admin@email.com",
        password="testPassword123")


@pytest.fixture
def testUser1() -> User:
    """
    Generate a user
    """
    return User.objects.create_user(
        username="testUser1",
        email="admin@email123.com",
        password="testPassword123")


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
def testViewTest(testUser: User, testUser1: User) -> TweetItemViewSet:
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
    return TweetItemViewSet()
