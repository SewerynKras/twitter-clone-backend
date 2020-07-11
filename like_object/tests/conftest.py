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
        text="Test tweet 1!",
        author=testUser0,
        uuid="11111111-1111-1111-1111-111111111111")
    tweet2 = TweetObject.objects.create(
        text="Test tweet 2!",
        author=testUser1,
        uuid="22222222-2222-2222-2222-222222222222")
    like1 = LikeObject.objects.create(
        tweet=tweet1, author=testUser1
    )
    like2 = LikeObject.objects.create(
        tweet=tweet2, author=testUser0
    )
