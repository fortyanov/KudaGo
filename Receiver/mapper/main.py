__author__ = 'Fedor Ortyanov fortyanov@gmail.com'

################## SIMPLE MAPPER json/xml TO MODULES #######################


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
        self.ser_data = r.text
        self.contype = r.headers['content-type']
        self.trash_fields = trash_fields.split('.') if type(trash_fields) == str else trash_fields
        self.success = False

    @property
    def data(self):
        if 'json' in self.contype:
            data = json.loads(self.ser_data)

        elif 'xml' in self.contype:
            xmldoc = xmltodict.parse(self.ser_data)
            try:
                for field in self.trash_fields: xmldoc = xmldoc[field]
                data = [dict(obj) for obj in xmldoc]
            except (ValueError, TypeError, KeyError):
                raise WrongTrashField

        else:
            raise WrongContent

        return data


    def fill_model(self):
        model = data = ''
        info = 'There is no comparable models for such data.'
        try:
            data = self.data    # data = list of dicts
        except (WrongTrashField, WrongContent) as e:
            info = e.info
        if data:
            for sd in data:    # sd - dict with serialized data for one object
                if 'id' in sd: del sd['id']
                for m in ALL_MODELS:
                    try:
                        m.objects.create(**sd)
                        self.success = True
                        model = m.__name__
                        info = 'The mapping operation was successful.'
                        break
                    except: pass

        print('data: %s\nurl: %s\nmodel: %s\nsuccess: %s\ntrash_fields: %s\ninfo: %s' %
              (self.ser_data, self.url, model, self.success, ('.'.join(self.trash_fields)), info))
        MapperStat.objects.create(data=self.ser_data,
                                  url=self.url,
                                  model=model,
                                  success=self.success,
                                  trash_fields='.'.join(self.trash_fields),
                                  info=info)