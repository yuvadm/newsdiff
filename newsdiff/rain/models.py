from django.db import models


class RainRadarImage(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to='rain/%Y/%m/%d')

    def __unicode__(self):
        return self.created.strftime('%Y/%m/%d %H:%M')
