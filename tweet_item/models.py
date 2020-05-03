import uuid
from django.db import models


class TweetItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=256)
    author = models.ForeignKey(
        'auth.User',
        related_name='tweets',
        on_delete=models.CASCADE)
