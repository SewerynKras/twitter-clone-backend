import pytest
from django.contrib.auth.models import User
from like_object.models import LikeObject
from user_profile.models import Profile
from tweet_object.models import TweetObject
from backend.tests.conftest import *

pytestmark = pytest.mark.django_db


@pytest.fixture
def testViewSet(testUser0: Profile, testUser1: Profile) -> None:
    """
    Creates 3 TweetObjects and 2 LikeObjects
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
