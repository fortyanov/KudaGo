__author__ = 'Fedor Ortyanov fortyanov@gmail.com'

################## SIMPLE MAPPER MODULE #######################


import json
import requests
import xmltodict
from mapper.errors import *
from mapper.models import *
from django.apps import apps


ALL_MODELS = apps.get_models()     # i like new django 1.7 stuff


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
        info = model = ser_data = ''
        try:
            ser_data = self.serialized_data
        except (WrongTrashField, WrongContent) as e:
            info = e.info
        if ser_data:
            for sd in ser_data:
                if 'id' in sd: del sd['id']
                for m in ALL_MODELS:
                    try:
                        m.objects.create(**sd)
                        self.success = True
                        model = m.__name__
                        break
                    except: pass

        print('data: %s\nurl: %s\nmodel: %s\nsuccess: %s\ntrash_fields: %s\ninfo: %s' % (self.data, self.url, model, self.success, ('.'.join(self.trash_fields)), info))
        MapperStat.objects.create(data=self.data,
                                  url=self.url,
                                  model=model,
                                  success=self.success,
                                  trash_fields='.'.join(self.trash_fields),
                                  info=info)