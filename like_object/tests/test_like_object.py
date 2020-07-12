from django.urls import reverse
import pytest
from user_profile.models import Profile
from user_profile.views import ProfileViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_get(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/11111111-1111-1111-1111-111111111111/likes/")
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['username'] == "testUser1"


def test_01_correct_get_no_auth(APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get(
        "/tweets/11111111-1111-1111-1111-111111111111/likes/")
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['username'] == "testUser1"


def test_02_correct_post(APIClient, testViewSet):
    data = {"tweet_id": "11111111-1111-1111-1111-111111111111"}
    response = APIClient.post("/likes/", data)
    assert response.status_code == 201

    # Check that it got created
    response = APIClient.get(
        "/tweets/11111111-1111-1111-1111-111111111111/likes/")
    assert response.status_code == 200
    assert response.json()['count'] == 2


def test_03_incorrect_post_no_auth(APIClient_no_auth, testViewSet):
    data = {"tweet_id": "11111111-1111-1111-1111-111111111111"}
    response = APIClient_no_auth.post("/likes/", data)
    assert response.status_code == 401


def test_04_incorrect_post_duplicate(APIClient, testViewSet):
    data = {"tweet_id": "22222222-2222-2222-2222-222222222222"}
    response = APIClient.post("/likes/", data)
    assert response.status_code == 400


def test_05_incorrect_post_not_found(APIClient, testViewSet):
    data = {"tweet_id": "66666666-6666-6666-6666-666666666666"}
    response = APIClient.post("/likes/", data)
    assert response.status_code == 400


def test_06_correct_delete(APIClient, testViewSet):
    response = APIClient.delete("/likes/22222222-2222-2222-2222-222222222222/")
    assert response.status_code == 204

    # Check that it got deleted
    response = APIClient.get(
        "/tweets/22222222-2222-2222-2222-222222222222/likes/")
    assert response.status_code == 200
    assert response.json()['count'] == 0


def test_07_incorrect_delete_like_not_found(APIClient, testViewSet):
    response = APIClient.delete("/likes/11111111-1111-1111-1111-111111111111/")
    assert response.status_code == 404


def test_08_incorrect_delete_tweet_not_found(APIClient, testViewSet):
    response = APIClient.delete("/likes/66666666-6666-6666-6666-666666666666/")
    assert response.status_code == 404
