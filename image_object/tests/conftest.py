import pytest
from django.contrib.auth.models import User
from user_profile.models import Profile
from backend.tests.conftest import *


pytestmark = pytest.mark.django_db
