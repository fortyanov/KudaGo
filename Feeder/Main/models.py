from django.db.models import *
import datetime

class SomeData(Model):
    title = CharField(max_length=100)
    link = CharField(max_length=100)
    description = CharField(max_length=100)

    author = CharField(max_length=100, blank=True)
    category = CharField(max_length=100, blank=True)
    comments = CharField(max_length=100, blank=True)
    pubDate = DateTimeField(default=datetime.datetime.now())
    placement = CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
