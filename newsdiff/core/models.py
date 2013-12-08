from django.db import models
from django.utils.timezone import now as tz_now


class HaaretzArticle(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=300)
    text = models.TextField()
    date = models.DateTimeField()


class HaaretzImage(models.Model):
    article = models.ForeignKey(HaaretzArticle)
    origin_url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/haaretz')
