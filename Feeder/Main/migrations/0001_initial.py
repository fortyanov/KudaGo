# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SomeData',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100, blank=True)),
                ('category', models.CharField(max_length=100, blank=True)),
                ('comments', models.CharField(max_length=100, blank=True)),
                ('pubDate', models.DateTimeField(default=datetime.datetime(2015, 3, 15, 17, 36, 27, 879751))),
                ('placement', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
