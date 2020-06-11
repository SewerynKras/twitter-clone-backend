from django.urls import reverse
import pytest
from tweet_item.models import TweetItem
from tweet_item.views import TweetItemViewSet
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_00_correct_list(APIClient, testViewTest):
    response = APIClient.get("/tweets/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 4


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


def test_11_correct_get_retweet_id(APIClient, testViewTest):
    response = APIClient.get("/tweets/4/")
    assert response.status_code == 200
    assert response.json()['retweet'] == 3


def test_12_incorrect_get_retweet_id_not_found(APIClient, testViewTest):
    response = APIClient.get("/tweets/2/retweet/")
    assert response.status_code == 404


def test_13_correct_get_retweet_detail(APIClient, testViewTest):
    response = APIClient.get("/tweets/4/retweet/")
    response1 = APIClient.get("/tweets/3/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_14_correct_get_no_auth(APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/tweets/4/")
    assert response.status_code == 200
    assert response.json()['retweet'] == 3


def test_15_correct_get_detail_no_auth(APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/tweets/4/retweet/")
    response1 = APIClient_no_auth.get("/tweets/3/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_16_correct_post_with_retweet(APIClient):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {
        "retweet_id": response.json()['id'],
        "text": "Look at this cool retweet"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 201


def test_17_correct_post_with_retweet_no_text(APIClient):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {"retweet_id": response.json()['id']}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 201


def test_18_incorrect_post_not_found(APIClient, testViewTest):
    data = {"tweet_id": 1234}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400


def test_19_correct_get_comment_id(APIClient, testViewTest):
    response = APIClient.get("/tweets/5/")
    assert response.status_code == 200
    assert response.json()['comment'] == 2


def test_20_correct_get_comment_num(APIClient, testViewTest):
    response = APIClient.get("/tweets/5/")
    assert response.status_code == 200
    assert response.json()['comments'] == 1


def test_21_incorrect_get_retweet_id_not_found(APIClient, testViewTest):
    response = APIClient.get("/tweets/2/retweet/")
    assert response.status_code == 404


def test_22_correct_get_comment_detail(APIClient, testViewTest):
    response = APIClient.get("/tweets/5/comment/")
    response1 = APIClient.get("/tweets/2/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_23_correct_post_with_comment(APIClient):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {
        "commnet_id": response.json()['id'],
        "text": "Look at this cool comment"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 201


def test_24_incorrect_post_with_comment_no_text(APIClient):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {"comment_id": response.json()['id']}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400


def test_25_incorrect_post_comment_not_found(APIClient, testViewTest):
    data = {"comment_id": 1234, "text": "Look at this awesome comment"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400
