from django.urls import reverse
import pytest
from tweet_object.models import TweetObject
from tweet_object.views import TweetObjectViewSet
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


pytestmark = pytest.mark.django_db


def test_00_correct_list(APIClient, testViewSet):
    response = APIClient.get("/tweets/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 6


def test_01_correct_get_single_mine(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/11111111-1111-1111-1111-111111111111/")
    assert response.status_code == 200
    assert response.json()['text'] == "Test tweet 1!"


def test_02_correct_get_single_not_mine(APIClient, testViewSet):
    response = APIClient.get("/tweets/33333333-3333-3333-3333-333333333333/")
    assert response.status_code == 200
    assert response.json()['text'] == "Test tweet 3!"


def test_03_correct_get_single_text(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/11111111-1111-1111-1111-111111111111/text/")
    assert response.status_code == 200
    assert response.json() == "Test tweet 1!"


def test_04_correct_post_single(APIClient):
    data = {"text": "New tweet"}
    response = APIClient.post("/tweets/", data, format='json')
    assert response.status_code == 201


def test_05_correct_put(APIClient, testViewSet):
    data = {"text": "Different tweet now!"}
    response = APIClient.put(
        "/tweets/11111111-1111-1111-1111-111111111111/",
        data)
    assert response.status_code == 200


def test_06_incorrect_put_not_found(APIClient, testViewSet):
    data = {"text": "Different tweet now!"}
    response = APIClient.put(
        "/tweets/12345678-9876-5432-1234-567898765432/")
    assert response.status_code == 404


def test_07_incorrect_put_not_authorized(APIClient, testViewSet):
    data = {"text": "Different tweet now!"}
    response = APIClient.put(
        "/tweets/33333333-3333-3333-3333-333333333333/")
    assert response.status_code == 403


def test_08_correct_delete(APIClient, testViewSet):
    response = APIClient.delete(
        "/tweets/11111111-1111-1111-1111-111111111111/")
    assert response.status_code == 204


def test_09_incorrect_delete_not_found(APIClient, testViewSet):
    response = APIClient.delete(
        "/tweets/12345678-9876-5432-1234-567898765432/",)
    assert response.status_code == 404


def test_10_incorrect_delete_not_authorized(APIClient, testViewSet):
    response = APIClient.delete(
        "/tweets/33333333-3333-3333-3333-333333333333/")
    assert response.status_code == 403


def test_11_correct_get_retweet_id(APIClient, testViewSet):
    response = APIClient.get("/tweets/44444444-4444-4444-4444-444444444444/")
    assert response.status_code == 200
    assert response.json()['retweet'] == 3


def test_12_incorrect_get_retweet_id_not_found(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/22222222-2222-2222-2222-222222222222/retweet/")
    assert response.status_code == 404


def test_13_correct_get_retweet_detail(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/44444444-4444-4444-4444-444444444444/retweet/")
    response1 = APIClient.get("/tweets/33333333-3333-3333-3333-333333333333/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_14_correct_get_no_auth(APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get(
        "/tweets/44444444-4444-4444-4444-444444444444/")
    assert response.status_code == 200
    assert response.json()['retweet'] == 3


def test_15_correct_get_detail_no_auth(APIClient_no_auth, testViewSet):
    response = APIClient_no_auth.get(
        "/tweets/44444444-4444-4444-4444-444444444444/retweet/")
    response1 = APIClient_no_auth.get(
        "/tweets/33333333-3333-3333-3333-333333333333/")
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


def test_18_incorrect_post_not_found(APIClient, testViewSet):
    data = {"retweet_id": "12345678-9876-5432-1234-567898765432"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400


def test_19_correct_get_comment_id(APIClient, testViewSet):
    response = APIClient.get("/tweets/55555555-5555-5555-5555-555555555555/")
    assert response.status_code == 200
    assert response.json()['comment'] == 2


def test_20_correct_get_comment_num(APIClient, testViewSet):
    response = APIClient.get("/tweets/55555555-5555-5555-5555-555555555555/")
    assert response.status_code == 200
    assert response.json()['comments'] == 1


def test_21_incorrect_get_retweet_id_not_found(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/22222222-2222-2222-2222-222222222222/retweet/")
    assert response.status_code == 404


def test_22_correct_get_comment_detail(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/55555555-5555-5555-5555-555555555555/comment/")
    response1 = APIClient.get("/tweets/22222222-2222-2222-2222-222222222222/")
    assert response.status_code == 200
    assert response.json() == response1.json()


def test_23_correct_post_with_comment(APIClient):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {
        "comment_id": response.json()['id'],
        "text": "Look at this cool comment"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 201


def test_24_incorrect_post_with_comment_no_text(APIClient):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {"comment_id": response.json()['id']}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400


def test_25_incorrect_post_comment_not_found(APIClient):
    data = {"comment_id": "12345678-9876-5432-1234-567898765432",
            "text": "Look at this awesome comment"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400


def test_26_incorrect_post_comment_and_retweet(APIClient, testViewSet):
    data = {"comment_id": "11111111-1111-1111-1111-111111111111",
            "retweet_id": "22222222-2222-2222-2222-222222222222",
            "text": "Look at this awesome comment"}
    response = APIClient.post("/tweets/", data)
    assert response.status_code == 400


def test_27_incorrect_get_comment_not_found(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/22222222-2222-2222-2222-222222222222/comment/")
    assert response.status_code == 404


def test_28_correct_post_with_file(APIClient, mockImageUpload, dummyImage):
    data = {"text": "New tweet", "image": dummyImage}
    response = APIClient.post("/tweets/", data, format='multipart')
    assert response.status_code == 201


def test_29_correct_post_with_file_and_comment(
        APIClient, mockImageUpload, dummyImage):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post(
        "/tweets/", data, format='json')

    data = {
        "comment_id": response.json()['id'],
        "text": "New tweet",
        "image": dummyImage
    }
    response = APIClient.post("/tweets/", data, format='multipart')
    assert response.status_code == 201


def test_30_correct_post_with_file_and_comment(
        APIClient, mockImageUpload, dummyImage):
    data = {"text": "Look at this cool tweet"}
    response = APIClient.post("/tweets/", data)

    data = {
        "retweet_id": response.json()['id'],
        "text": "New tweet",
        "image": dummyImage
    }
    response = APIClient.post("/tweets/", data, format='multipart')
    assert response.status_code == 201


def test_31_correct_get_with_file(APIClient, testViewSet, mockImageUpload):
    response = APIClient.get("/tweets/22222222-2222-2222-2222-222222222222/")
    assert response.status_code == 200
    assert response.json()[
        'image_url'] == "https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg"


def test_32_correct_get_comments(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/55555555-5555-5555-5555-555555555555/comments/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 1


def test_33_correct_get_comments_0(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/11111111-1111-1111-1111-111111111111/comments/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 0


def test_34_correct_get_retweets(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/33333333-3333-3333-3333-333333333333/retweets/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 1


def test_35_correct_get_retweets_0(APIClient, testViewSet):
    response = APIClient.get(
        "/tweets/11111111-1111-1111-1111-111111111111/retweets/")
    assert response.status_code == 200
    assert len(response.json()['results']) == 0
