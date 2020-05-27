from django.urls import reverse
import pytest
from user_profile.models import Profile
from user_profile.views import ProfileViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_get_my_following(APIClient, testViewTest):
    response = APIClient.get("/user/1/following/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 1


def test_01_correct_get_my_followers(APIClient, testViewTest):
    response = APIClient.get("/user/1/followers/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 1


def test_02_correct_get_someones_following(APIClient, testViewTest):
    response = APIClient.get("/user/2/following/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 1


def test_03_correct_get_someones_followers(APIClient, testViewTest):
    response = APIClient.get("/user/2/followers/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 2


def test_04_correct_get_someones_following_no_auth(
        APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/user/1/following/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 1


def test_05_correct_get_someones_followers_no_auth(
        APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/user/1/followers/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 2


def test_06_correct_post(APIClient, testViewTest):
    data = {"id": 3}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 201


def test_07_incorrect_post_myself(APIClient, testViewTest):
    data = {"id": 1}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_08_incorrect_post_already_following(APIClient, testViewTest):
    data = {"id": 2}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_09_incorrect_post_no_auth(APIClient_no_auth, testViewTest):
    data = {"id": 2}
    response = APIClient_no_auth.post("/follow/", data)
    assert response.status_code == 403


def test_10_correct_delete(APIClient, testViewTest):
    data = {"id": 2}
    response = APIClient.delete("/follow/", data)
    assert response.status_code == 200


def test_11_incorrect_delete_not_following(APIClient, testViewTest):
    data = {"id": 3}
    response = APIClient.delete("/follow/", data)
    assert response.status_code == 400
