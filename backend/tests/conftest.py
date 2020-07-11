"""
Pytest fixtures defined in this file are designed to be reusable across different modules.
No actual tests are defined here.
"""
import pytest
from django.contrib.auth.models import User
from follow_object.views import FollowObjectViewSet
from follow_object.models import FollowObject
from user_profile.models import Profile
from image_object.models import ImageObject


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
def testUser2() -> Profile:
    """
    Generate a user
    """
    user = User.objects.create_user(
        username="testUser2",
        email="admin@email123.com",
        password="testPassword123",
        id=3)
    profile = Profile.objects.create(
        user=user,
        display_name="testUser2 name",
        id=3)

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
    with testUser0
    """
    from rest_framework.test import APIClient
    client = APIClient()
    data = {"username": "testUser", "password": "testPassword123"}
    resp = client.post("/token/", data=data, follow=True)
    token = resp.data["access"]
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return client
