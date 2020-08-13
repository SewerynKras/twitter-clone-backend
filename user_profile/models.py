from django.db import models
from django.contrib.auth.models import User
from follow_object.models import FollowObject
from django.db.models import Count


class FollowersManager(models.Manager):
    """
    Annotates the number of followers to the queryset
    """

    def get_queryset(self):
        return super(
            FollowersManager,
            self).get_queryset().annotate(
            followers=Count("being_followed"))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    image = models.ForeignKey(
        'image_object.ImageObject',
        null=True,
        default=None,
        on_delete=models.CASCADE
    )
    objects = FollowersManager()

    class Meta:
        # Number of followers gets annotated by the FollowersManager
        ordering = ['-followers']
