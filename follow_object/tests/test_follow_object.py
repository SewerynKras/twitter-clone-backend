from django.urls import reverse
import pytest
from user_profile.models import Profile
from user_profile.views import ProfileViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_get_my_following(APIClient, testViewSet):
    response = APIClient.get("/users/testUser/following/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_01_correct_get_my_followers(APIClient, testViewSet):
    response = APIClient.get("/users/testUser/followers/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_02_correct_get_someones_following(APIClient, testViewSet):
    response = APIClient.get("/users/testUser1/following/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_03_correct_get_someones_followers(APIClient, testViewSet):
    response = APIClient.get("/users/testUser1/followers/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_04_correct_get_someones_following_no_auth(
        APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get("/users/testUser1/following/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_05_correct_get_someones_followers_no_auth(
        APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get("/users/testUser1/followers/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_06_correct_post(APIClient, testViewSet):
    data = {"being_followed": "testUser2"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 201


def test_07_incorrect_post_myself(APIClient, testViewSet):
    data = {"being_followed": "testUser"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_08_incorrect_post_already_following(APIClient, testViewSet):
    data = {"being_followed": "testUser1"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_09_incorrect_post_no_auth(APIClient_no_auth, testViewSet):
    data = {"being_followed": 2}
    response = APIClient_no_auth.post("/follow/", data)
    assert response.status_code == 401


def test_10_correct_delete(APIClient, testViewSet):
    response = APIClient.delete("/follow/2/")
    assert response.status_code == 204


def test_11_incorrect_delete_not_following(APIClient, testViewSet):
    response = APIClient.delete("/follow/3/")
    assert response.status_code == 404
