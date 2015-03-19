from django.db.models import *


class MapperStat(Model):                             # drop loading data information to this table
    data = TextField(blank=True)
    url = URLField()
    model = CharField(max_length=100, blank=True)
    trash_fields = CharField(max_length=100, blank=True)
    success = BooleanField(default=False)
    info = TextField(blank=True)
    timestamp = DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s' % (self.success, self.timestamp)
