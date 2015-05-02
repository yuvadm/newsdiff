# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, default='(untitled)')),
                ('url', models.URLField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('document', models.FileField(upload_to='documents')),
            ],
        ),
    ]
