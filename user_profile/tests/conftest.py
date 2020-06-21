import tempfile
from unittest.mock import Mock

import cloudinary.uploader
import pytest
from django.contrib.auth.models import User
from PIL import Image

from image_object.models import ImageObject
from user_profile.models import Profile
from user_profile.views import ProfileViewSet

pytestmark = pytest.mark.django_db


@pytest.fixture
def testUser() -> Profile:
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
        id=2
    )
    image = ImageObject.objects.create(
        public_id='hl22acprlomnycgiudor',
        url='https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        height=282,
        width=292,
        format='jpg',
        author=profile)
    profile.image = image
    profile.save()
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
    Generate a rest_frameworks APICLient but doesn't authenticate it
    """
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture
def testViewTest(testUser: Profile, testUser1: Profile) -> ProfileViewSet:
    """
    Creates 2 Profiles and returns a
    ProfileViewSet instance
    """
    return ProfileViewSet()


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
