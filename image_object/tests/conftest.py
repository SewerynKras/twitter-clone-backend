import pytest
from django.contrib.auth.models import User
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
        password="testPassword123",
        id=1)
    profile = Profile.objects.create(
        user=user,
        display_name="testUser name",
        id=1
    )
    return profile
