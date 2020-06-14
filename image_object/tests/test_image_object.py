import pytest
import cloudinary.uploader
from tempfile import TemporaryFile
from unittest.mock import Mock

pytestmark = pytest.mark.django_db


def test_00_correct_create():
    mock_response = {
        'public_id': 'mock-public-id',
        'secure_url': 'someurl.com/something',
    }
    cloudinary.uploader.upload = Mock(
        side_effect=lambda *args: mock_response)

    with TemporaryFile() as tmp:
        file = ImageObject(file=tmp)
        file.save()
        assert cloudinary.uploader.upload.called
        assert file.public_id == 'mock-public-id'
        assert file.secure_url == 'someurl.com/something'
