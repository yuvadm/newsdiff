from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now as tz_now


class NewsDiffUser(AbstractUser):
    pass


class HaaretzArticle(models.Model):
    url = models.CharField(max_length=250)
    haaretz_id = models.CharField(max_length=12, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=1000, blank=True, null=True)
    author = models.CharField(max_length=60)
    text = models.TextField()
    date = models.DateTimeField()

    def __unicode__(self):
        return self.url


class HaaretzImage(models.Model):
    article = models.ForeignKey(HaaretzArticle, related_name='images')
    origin_url = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/haaretz')
    caption = models.CharField(max_length=140, blank=True, null=True)

    def __unicode__(self):
        return self.origin_url
