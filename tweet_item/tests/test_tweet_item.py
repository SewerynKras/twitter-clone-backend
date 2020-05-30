from django.urls import reverse
import pytest
from tweet_item.models import TweetItem
from tweet_item.views import TweetItemViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_list(APIClient, testViewTest):
    response = APIClient.get("/tweets/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 3


def test_01_correct_get_single_mine(APIClient, testViewTest):
    response = APIClient.get("/tweets/1", follow=True)
    assert response.status_code == 200
    assert response.json()['text'] == "Test tweet 1!"


def test_02_correct_get_single_not_mine(APIClient, testViewTest):
    response = APIClient.get("/tweets/3", follow=True)
    assert response.status_code == 200
    assert response.json()['text'] == "Test tweet 3!"


def test_03_correct_get_single_text(APIClient, testViewTest):
    response = APIClient.get("/tweets/1/text", follow=True)
    assert response.status_code == 200
    assert response.json() == "Test tweet 1!"


def test_04_correct_post_single(APIClient):
    data = {"text": "New tweet"}
    response = APIClient.post("/tweets/", data, format='json')
    assert response.status_code == 201


def test_05_correct_put(APIClient, testViewTest):
    data = {"text": "Different tweet now!"}
    response = APIClient.put("/tweets/1/", data, follow=True)
    assert response.status_code == 200


def test_06_incorrect_put_not_found(APIClient, testViewTest):
    data = {"text": "Different tweet now!"}
    response = APIClient.put("/tweets/1000/", follow=True)
    assert response.status_code == 404


def test_07_incorrect_put_not_authorized(APIClient, testViewTest):
    data = {"text": "Different tweet now!"}
    response = APIClient.put("/tweets/3/", follow=True)
    assert response.status_code == 403


def test_08_correct_delete(APIClient, testViewTest):
    response = APIClient.delete("/tweets/1/", follow=True)
    assert response.status_code == 204


def test_09_incorrect_delete_not_found(APIClient, testViewTest):
    response = APIClient.delete("/tweets/1000/", follow=True)
    assert response.status_code == 404


def test_10_incorrect_delete_not_authorized(APIClient, testViewTest):
    response = APIClient.delete("/tweets/3/", follow=True)
    assert response.status_code == 403
