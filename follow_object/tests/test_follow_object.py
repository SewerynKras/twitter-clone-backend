from django.urls import reverse
import pytest
from user_profile.models import Profile
from user_profile.views import ProfileViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_get_my_following(APIClient, testViewSet):
    response = APIClient.get("/users/profile/testUser/following/")
    assert response.status_code == 200
    assert response.json()['count'] == 1


def test_01_correct_get_my_followers(APIClient, testViewSet):
    response = APIClient.get("/users/profile/testUser/followers/")
    assert response.status_code == 200
    assert response.json()['count'] == 1


def test_02_correct_get_someones_following(APIClient, testViewSet):
    response = APIClient.get("/users/profile/testUser1/following/")
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['username'] == "testUser2"


def test_03_correct_get_someones_followers(APIClient, testViewSet):
    response = APIClient.get("/users/profile/testUser1/followers/")
    assert response.status_code == 200
    assert response.json()['count'] == 2


def test_04_correct_get_someones_following_no_auth(
        APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get("/users/profile/testUser1/following/")
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['username'] == "testUser2"


def test_05_correct_get_someones_followers_no_auth(
        APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get("/users/profile/testUser/followers/")
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['username'] == "testUser2"


def test_06_correct_post(APIClient, testViewSet):
    data = {"being_followed": "testUser2"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 201
    assert response.json()['created']


def test_07_incorrect_post_myself(APIClient, testViewSet):
    data = {"being_followed": "testUser"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_08_incorrect_post_already_following(APIClient, testViewSet):
    data = {"being_followed": "testUser1"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_09_incorrect_post_not_found(APIClient, testViewSet):
    data = {"being_followed": "testUser123456789"}
    response = APIClient.post("/follow/", data)
    assert response.status_code == 400


def test_10_incorrect_post_no_auth(APIClient_no_auth, testViewSet):
    data = {"being_followed": "testUser1"}
    response = APIClient_no_auth.post("/follow/", data)
    assert response.status_code == 401


def test_11_correct_delete(APIClient, testViewSet):
    response = APIClient.delete("/follow/testUser1/")
    assert response.status_code == 204


def test_12_incorrect_delete_not_following(APIClient, testViewSet):
    response = APIClient.delete("/follow/testUser2/")
    assert response.status_code == 404


def test_13_correct_get_recommendations(APIClient, testViewSet):
    response = APIClient.get("/follow/getRecommendations/")
    assert response.status_code == 200
    assert response.json()['results'][0]['username'] == "testUser1"
