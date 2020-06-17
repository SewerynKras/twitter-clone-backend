import pytest
import cloudinary.uploader
from tempfile import TemporaryFile
from unittest.mock import Mock
from image_object.models import ImageObject


pytestmark = pytest.mark.django_db


def test_00_correct_create(testUser):
    mock_response = {
        u'bytes': 29802,
        u'created_at': u'2017-06-25T17:20:30Z',
        u'format': u'jpg',
        u'height': 282,
        u'public_id': u'hl22acprlomnycgiudor',
        u'resource_type': u'image',
        u'secure_url': u'https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        u'signature': u'10594f028dbc23e920fd084f8482394798edbc68',
        u'type': u'upload',
        u'url': u'http://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg',
        u'version': 1571218039,
        u'width': 292}
    cloudinary.uploader.upload = Mock(
        side_effect=lambda *args: mock_response)

    with TemporaryFile() as tmp:
        file = ImageObject(author=testUser)
        file.upload(tmp)
        file.save()
        assert cloudinary.uploader.upload.called
        assert file.public_id == 'hl22acprlomnycgiudor'
        assert file.url == 'https://res.cloudinary.com/demo/image/upload/v1571218039/hl22acprlomnycgiudor.jpg'
        assert file.height == 282
        assert file.width == 292
        assert file.format == 'jpg'
        assert file.author == testUser
