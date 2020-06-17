from django.db import models
import cloudinary.uploader


class ImageObject(models.Model):
    public_id = models.CharField(max_length=128)
    format = models.CharField(max_length=10)
    url = models.URLField()
    author = models.ForeignKey(
        "user_profile.Profile",
        on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def upload(self, file):
        response = cloudinary.uploader.upload(file)
        self.public_id = response['public_id']
        self.url = response['secure_url']
        self.height = response['height']
        self.width = response['width']
        self.format = response['format']
