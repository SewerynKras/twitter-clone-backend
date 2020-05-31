from django.db import models


class LikeObject(models.Model):
    tweet = models.ForeignKey(
        'tweet_item.TweetItem',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        'user_profile.Profile',
        on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
