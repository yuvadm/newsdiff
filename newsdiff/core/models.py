import reversion

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
    author = models.CharField(max_length=120)
    text = models.TextField()
    date = models.DateTimeField()
    starred = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url

reversion.register(HaaretzArticle)


class HaaretzImage(models.Model):
    article = models.ForeignKey(HaaretzArticle, related_name='images')
    origin_url = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/haaretz')
    caption = models.CharField(max_length=140, blank=True, null=True)

    def __unicode__(self):
        return self.origin_url


class YnetArticle(models.Model):
    url = models.CharField(max_length=250)
    ynet_id = models.CharField(max_length=9, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=1000, blank=True, null=True)
    author = models.CharField(max_length=60)
    text = models.TextField()
    date = models.DateTimeField()

    def __unicode__(self):
        return self.url

reversion.register(YnetArticle)


class YnetImage(models.Model):
    article = models.ForeignKey(YnetArticle, related_name='images')
    origin_url = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/ynet')
    caption = models.CharField(max_length=140, blank=True, null=True)

    def __unicode__(self):
        return self.origin_url
