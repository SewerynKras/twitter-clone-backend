import tempfile
from unittest.mock import Mock

import cloudinary.uploader
import pytest
from django.contrib.auth.models import User
from PIL import Image

from image_object.models import ImageObject
from tweet_object.models import TweetObject
from user_profile.models import Profile
from backend.tests.conftest import *

pytestmark = pytest.mark.django_db


@pytest.fixture
def testViewSet(testUser0: Profile, testUser1: Profile) -> None:
    """
    Creates 6 TweetObjects
    """
    image1 = ImageObject.objects.create(
        public_id='hl22acprlomnycgiudor',
        url='https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        height=282,
        width=292,
        format='jpg',
        author=testUser0)
    tweet1 = TweetObject.objects.create(
        text="Test tweet 1!", author=testUser0, id="1")
    tweet2 = TweetObject.objects.create(
        text="Test tweet 2!", author=testUser0, id="2", image=image1)
    tweet3 = TweetObject.objects.create(
        text="Test tweet 3!", author=testUser1, id="3")
    tweet4 = TweetObject.objects.create(
        text="I am a retweet 1!",
        author=testUser0, id="4", retweet=tweet3)
    tweet5 = TweetObject.objects.create(
        text="I am a comment 1!",
        author=testUser1, id="5", comment=tweet2)
    tweet6 = TweetObject.objects.create(
        text="I am a comment 2!",
        author=testUser1, id="6", comment=tweet5)


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
