import pytest

pytestmark = pytest.mark.django_db


def test_00_correct_get_retweet_id(APIClient, testViewTest):
    response = APIClient.get("/tweets/2/")
    assert response.status_code == 200
    assert response.json()['retweet'] == 1


def test_01_correct_get_detail(APIClient, testViewTest):
    response = APIClient.get("/tweets/2/retweet/")
    response1 = APIClient.get("/tweets/1/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_02_correct_get_no_auth(APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/tweets/2/")
    assert response.status_code == 200
    assert response.json()['retweet'] == 1


def test_03_correct_get_detail_no_auth(APIClient_no_auth, testViewTest):
    response = APIClient_no_auth.get("/tweets/2/retweet/")
    response1 = APIClient_no_auth.get("/tweets/1/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_04_correct_post_no_text(APIClient, testViewTest):
    data = {"tweet_id": 3}
    response = APIClient.post("/retweets/", data)
    assert response.status_code == 201


def test_05_correct_post(APIClient, testViewTest):
    data = {"tweet_id": 3, "text": "Look at this cool tweet"}
    response = APIClient.post("/retweets/", data)
    assert response.status_code == 201


def test_06_incorrect_post_no_text_no_auth(APIClient_no_auth, testViewTest):
    data = {"tweet_id": 3}
    response = APIClient_no_auth.post("/retweets/", data)
    assert response.status_code == 403


def test_07_incorrect_post_no_auth(APIClient_no_auth, testViewTest):
    data = {"tweet_id": 3, "text": "Look at this cool tweet"}
    response = APIClient_no_auth.post("/retweets/", data)
    assert response.status_code == 403


def test_08_incorrect_post_not_found_no_text(APIClient, testViewTest):
    data = {"tweet_id": 1234}
    response = APIClient.post("/retweets/", data)
    assert response.status_code == 400


def test_09_incorrect_post_not_found(APIClient, testViewTest):
    data = {"tweet_id": 1234, "text": "Look at this cool tweet"}
    response = APIClient.post("/retweets/", data)
    assert response.status_code == 400
