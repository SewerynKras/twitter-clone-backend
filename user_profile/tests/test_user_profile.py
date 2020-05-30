from django.urls import reverse
import pytest
from user_profile.models import Profile
from user_profile.views import ProfileViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_list(APIClient, testViewTest):
    response = APIClient.get("/users/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 2


def test_01_correct_get_single(APIClient, testViewTest):
    response = APIClient.get("/users/1/", follow=True)
    assert response.status_code == 200
    assert response.json()['username'] == 'testUser'
    assert ['id',
            'username',
            'display_name',
            'bio',
            'website',
            'location',
            'birth_date',
            'tweets'] == list(response.json().keys())


def test_02_incorrect_get_single_not_found(APIClient, testViewTest):
    response = APIClient.get("/users/123456/", follow=True)
    assert response.status_code == 404


def test_03_correct_post(APIClient_no_auth):
    data = {
        "username": "newUser",
        "display_name": "new user name",
        "password": "myNewCoolPassword123"
    }
    response = APIClient_no_auth.post("/users/", data)
    assert response.status_code == 201


def test_04_incorrect_post_duplicate(APIClient_no_auth, testViewTest):
    data = {
        "username": "testUser",
        "display_name": "new user name",
        "password": "myNewCoolPassword123"
    }
    response = APIClient_no_auth.post("/users/", data)
    assert response.status_code == 400


def test_05_incorrect_post_missing(APIClient_no_auth):
    data = {
        "username": "newUser",
        "display_name": "new user name",
        "password": ""
    }
    response = APIClient_no_auth.post("/users/", data)
    assert response.status_code == 400


def test_06_correct_patch(APIClient, testViewTest):
    data = {
        "username": "newUser1"
    }
    response = APIClient.patch("/users/1/", data)
    assert response.status_code == 200


def test_07_incorrect_patch_duplicate(APIClient, testViewTest):
    data = {
        "username": "testUser1"
    }
    response = APIClient.patch("/users/1/", data)
    assert response.status_code == 400


def test_08_incorrect_patch_no_auth(APIClient, testViewTest):
    data = {
        "username": "someOtherName"
    }
    response = APIClient.patch("/users/2/", data, follow=True)
    assert response.status_code == 403
