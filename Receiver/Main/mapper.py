__author__ = 'Fedor Ortyanov fortyanov@gmail.com'

################## SIMPLE MAPPER MODULE #######################

from django.db.models import get_models, get_app, Model, TextField, CharField, DateTimeField, BooleanField, URLField
import os
import json
import requests
import xmltodict


APP_NAME = os.path.dirname(__file__).split('/')[-1]
CURRENT_APP = get_app(APP_NAME)
MODELS_LIST = [model.__name__ for model in get_models(CURRENT_APP)]  # i used this variable to send on view for makeing select control on teamplate, but it is not needed anymore =(


class WrongTrashField(Exception):
    info = 'Wrong trash fields setup.\nReturned data cannot be represented as list of dictionaries.'


class WrongContent(Exception):
    info = 'Unsupported input data format.'


class MapperStat(Model):                             # drop loading data information to this table
    data = TextField(blank=True)
    url = URLField()
    model = CharField(max_length=100, blank=True)
    trash_fields = CharField(max_length=100, blank=True)
    success = BooleanField(default=False)
    info = TextField(blank=True)
    timestamp = DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s' % self.success, self.timestamp


class Mapper(object):
    def __init__(self, url, trash_fields=[]):
        self.url = url
        r = requests.get(url=url)
        self.data = r.text
        self.contype = r.headers['content-type']
        self.trash_fields = trash_fields.split('.') if type(trash_fields) == str else trash_fields
        self.success = False

    @property
    def serialized_data(self):
        if 'json' in self.contype:
            data = json.loads(self.data)

        elif 'xml' in self.contype:
            xmldoc = xmltodict.parse(self.data)
            for field in self.trash_fields: xmldoc = xmldoc[field]
            try:
                data = [dict(obj) for obj in xmldoc]
            except (ValueError, TypeError):
                raise WrongTrashField

        else:
            raise WrongContent

        return data


    def fill_model(self):
        model = None
        info = ''
        ser_data = self.serialized_data
        app_models = get_models(CURRENT_APP)
        for sd in ser_data:
            if 'id' in sd: del sd['id']
            print('sd: %s' % sd)
            for m in app_models:
                try:
                    m.objects.create(**sd)
                    self.success = True
                    model = m.__name__
                except WrongContent:
                    info = WrongContent.info
                except WrongTrashField:
                    info = WrongTrashField.info
                except: pass

        return MapperStat.objects.create(data=self.data,
                                         url=self.url,
                                         model=model,
                                         success=self.success,
                                         trash_fields='.'.join(self.trash_fields),
                                         info=info)