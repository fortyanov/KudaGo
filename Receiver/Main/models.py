from django.db.models import *
import datetime


class SomeData(Model):
    title = CharField(max_length=100)
    link = CharField(max_length=100)
    description = CharField(max_length=100)

    author = CharField(max_length=100, blank=True, null=True)
    category = CharField(max_length=100, blank=True, null=True)
    comments = CharField(max_length=100, blank=True, null=True)
    pubDate = DateTimeField(default=datetime.datetime.now()) # i know about auto_now, i did it just for fun
    placement = CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

