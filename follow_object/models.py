from django.db import models

# Create your models here.


class FollowObject(models.Model):
    following = models.ForeignKey(
        'user_profile.Profile',
        related_name='following',
        on_delete=models.CASCADE)
    being_followed = models.ForeignKey(
        'user_profile.Profile',
        related_name='being_followed',
        on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
