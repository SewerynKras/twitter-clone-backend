import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from user_profile.models import Profile
from user_profile.views import ProfileViewSet

pytestmark = pytest.mark.django_db


def test_00_correct_list(APIClient, testViewSet):
    response = APIClient.get("/users/profile/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 2


def test_01_correct_get_single(APIClient, testViewSet):
    response = APIClient.get("/users/profile/testUser/", follow=True)
    assert response.status_code == 200
    assert response.json()['username'] == 'testUser'
    assert sorted(['username',
                   'display_name',
                   'bio',
                   'website',
                   'location',
                   'birth_date',
                   'following',
                   'followers',
                   'image_url']) == sorted(list(response.json().keys()))


def test_02_incorrect_get_single_not_found(APIClient, testViewSet):
    response = APIClient.get("/users/profile/123456/", follow=True)
    assert response.status_code == 404


def test_03_correct_post(APIClient_no_auth):
    data = {
        "username": "newUser",
        "display_name": "new user name",
        "password": "myNewCoolPassword123"
    }
    response = APIClient_no_auth.post("/users/profile/", data)
    assert response.status_code == 201


def test_04_incorrect_post_duplicate(APIClient_no_auth, testViewSet):
    data = {
        "username": "testUser",
        "display_name": "new user name",
        "password": "myNewCoolPassword123"
    }
    response = APIClient_no_auth.post("/users/profile/", data)
    assert response.status_code == 400


def test_05_incorrect_post_missing(APIClient_no_auth):
    data = {
        "username": "newUser",
        "display_name": "new user name",
        "password": ""
    }
    response = APIClient_no_auth.post("/users/profile/", data)
    assert response.status_code == 400


def test_06_correct_patch(APIClient, testViewSet):
    data = {
        "username": "newUser1"
    }
    response = APIClient.patch("/users/profile/testUser/", data)
    assert response.status_code == 200


def test_07_incorrect_patch_duplicate(APIClient, testViewSet):
    data = {
        "username": "testUser1"
    }
    response = APIClient.patch("/users/profile/testUser/", data)
    assert response.status_code == 400


def test_08_incorrect_patch_no_auth(APIClient, testViewSet):
    data = {
        "username": "someOtherName"
    }
    response = APIClient.patch("/users/profile/testUser1/", data, follow=True)
    assert response.status_code == 403


def test_09_correct_post_with_image(
        APIClient_no_auth,
        dummyImage,
        mockImageUpload):
    data = {
        "username": "newUser",
        "display_name": "new user name",
        "password": "myNewCoolPassword123",
        "image": dummyImage
    }
    response = APIClient_no_auth.post("/users/profile/", data)
    assert response.status_code == 201


def test_10_correct_get_single_image(APIClient, testViewSet):
    response = APIClient.get("/users/profile/testUser1/", follow=True)
    assert response.status_code == 200
    assert response.json()[
        'image_url'] == 'https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg'


def test_11_correct_patch_with_image(
        APIClient,
        testViewSet,
        dummyImage,
        mockImageUpload):
    data = {
        "image": dummyImage
    }
    response = APIClient.patch("/users/profile/testUser/", data, format='multipart')
    assert response.status_code == 200


def test_12_incorrect_put(APIClient, testViewSet):
    data = {
        "username": "newUser1"
    }
    response = APIClient.put("/users/profile/testUser/", data)
    assert response.status_code == 405


def test_13_correct_get_my_profile(APIClient, testViewSet):
    response = APIClient.get("/users/getMyProfile/")
    assert response.status_code == 200
    assert response.json()['username'] == "testUser"
    assert response.json()['display_name'] == "testUser name"


def test_14_incorrect_get_my_profile_no_auth(APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get("/users/getMyProfile/")
    assert response.status_code == 401
