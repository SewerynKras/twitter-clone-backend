from django.urls import reverse
import pytest
from user_profile.models import Profile
from user_profile.views import ProfileViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_get(APIClient, testViewTest):
    response = APIClient.get("/tweets/1/likes/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()['author'] == "testUser0"


def test_01_correct_get_no_auth(APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/tweets/1/likes/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_02_correct_post(APIClient, testViewTest):
    data = {"tweet_id": 1}
    response = APIClient.post("/likes/", data)
    assert response.status_code == 201

    # Check that it got created
    response = APIClient.get("/tweets/1/likes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_03_incorrect_post_no_auth(APIClient_no_auth, testViewTest):
    data = {"tweet_id": 1}
    response = APIClient_no_auth.post("/likes/", data)
    assert response.status_code == 403


def test_04_incorrect_post_duplicate(APIClient, testViewTest):
    data = {"tweet_id": 2}
    response = APIClient.post("/likes/", data)
    assert response.status_code == 400


def test_05_incorrect_post_not_found(APIClient, testViewTest):
    data = {"tweet_id": 1234}
    response = APIClient.post("/likes/", data)
    assert response.status_code == 400


def test_06_correct_delete(APIClient, testViewTest):
    response = APIClient.delete("/likes/2/")
    assert response.status_code == 204

    # Check that it got deleted
    response = APIClient.get("/tweets/2/likes/")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_07_incorrect_delete_like_not_found(APIClient, testViewTest):
    response = APIClient.delete("/likes/1/")
    assert response.status_code == 404


def test_08_incorrect_delete_tweet_not_found(APIClient, testViewTest):
    response = APIClient.delete("/likes/1234/")
    assert response.status_code == 404
