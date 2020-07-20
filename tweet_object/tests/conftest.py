import tempfile
from unittest.mock import Mock

import cloudinary.uploader
import pytest
from django.contrib.auth.models import User
from PIL import Image

from backend.tests.conftest import *
from follow_object.models import FollowObject
from image_object.models import ImageObject
from like_object.models import LikeObject
from tweet_object.models import TweetObject
from user_profile.models import Profile

pytestmark = pytest.mark.django_db


@pytest.fixture
def testViewSet(testUser0: Profile, testUser1: Profile, testUser2) -> None:
    """
    Creates 6 TweetObjects and makes the testUser0 follow testUser2
    """
    image1 = ImageObject.objects.create(
        public_id='hl22acprlomnycgiudor',
        url='https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        height=282,
        width=292,
        format='jpg',
        author=testUser0)
    tweet1 = TweetObject.objects.create(
        text="Test tweet 1!",
        author=testUser0,
        uuid="11111111-1111-1111-1111-111111111111")
    tweet2 = TweetObject.objects.create(
        text="Test tweet 2!",
        author=testUser2,
        uuid="22222222-2222-2222-2222-222222222222",
        image=image1)
    tweet3 = TweetObject.objects.create(
        text="Test tweet 3!",
        author=testUser1,
        uuid="33333333-3333-3333-3333-333333333333")
    tweet4 = TweetObject.objects.create(
        text="I am a retweet 1!",
        author=testUser2,
        uuid="44444444-4444-4444-4444-444444444444",
        retweet=tweet3)
    tweet5 = TweetObject.objects.create(
        text="I am a comment 1!",
        author=testUser2,
        uuid="55555555-5555-5555-5555-555555555555",
        comment=tweet2)
    tweet6 = TweetObject.objects.create(
        text="I am a comment 2!",
        author=testUser1,
        uuid="66666666-6666-6666-6666-666666666666",
        comment=tweet5)
    tweet7 = TweetObject.objects.create(
        text="I am a retweet 2!",
        author=testUser0,
        uuid="77777777-7777-7777-7777-777777777777",
        retweet=tweet3)
    follow = FollowObject.objects.create(
        following=testUser0,
        being_followed=testUser2
    )
    like1 = LikeObject.objects.create(
        author=testUser0,
        tweet=tweet1
    )


@pytest.fixture
def dummyImage():
    """
    Returns a dummy image for upload testing purposes
    """
    image = Image.new('RGB', (100, 100))

    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)

    return tmp_file


@pytest.fixture
def mockImageUpload():
    """
    Mocks the cloudinary `upload` method with a sample response
    """
    mock_response = {
        u'bytes': 29802,
        u'created_at': u'2017-06-25T17:20:30Z',
        u'format': u'jpg',
        u'height': 282,
        u'public_id': u'hl22acprlomnycgiudor',
        u'resource_type': u'image',
        u'secure_url': u'https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        u'signature': u'10594f028dbc23e920fd084f8482394798edbc68',
        u'type': u'upload',
        u'url': u'http://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        u'version': 1571218039,
        u'width': 292}
    cloudinary.uploader.upload = Mock(
        side_effect=lambda *args: mock_response)
