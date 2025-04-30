from django.conf import settings
from django.db import models


# Create your models here.
class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    meta = models.CharField(max_length=300)
    content = models.TextField()
    thumbnail_img = models.ImageField(null=True, blank=True, upload_to="images/")
    thumbnail_path = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        if self.thumbnail_img:
            return f"{settings.MEDIA_URL}{self.thumbnail_img}"

        return self.thumbnail_path
