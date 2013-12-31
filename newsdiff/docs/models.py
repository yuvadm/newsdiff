from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=100, default='(untitled)')
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    document = models.FileField(upload_to='documents')

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.url)
