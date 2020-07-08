import pytest
from django.contrib.auth.models import User
from follow_object.views import FollowObjectViewSet
from follow_object.models import FollowObject
from user_profile.models import Profile
from backend.tests.conftest import *

pytestmark = pytest.mark.django_db


@pytest.fixture
def testViewSet(testUser0: Profile, testUser1: Profile,
                testUser2: Profile) -> None:
    """
    Creates 3 FollowObjects

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
