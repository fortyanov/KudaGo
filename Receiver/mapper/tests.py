from django.test import TestCase
from mapper.main import Mapper
import requests
from mapper import errors
from mapper.models import MapperStat


#                     NOTE
# You will need to have Feeder Django project launched
# on your pc with default port 8000 for use this tests.
#


class MapperTestCase(TestCase):
    # def setUp(self):
    #     map1 = Mapper(url='http://localhost:8000/xmldata/', trash_fields='root.list-item')


    def test_serialized_data(self):
        url1 = 'http://localhost:8000/xmldata/'
        url2 = 'http://localhost:8000/jsondata/'
        map1 = Mapper(url=url1, trash_fields='root.list-item')
        map2 = Mapper(url=url2)
        r1 = requests.get(url=url1)
        r2 = requests.get(url=url2)
        self.assertEqual(r1.headers['content-type'], map1.contype)
        self.assertEqual(r2.headers['content-type'], map2.contype)
        self.assertEqual(map1.ser_data, r1.text)
        self.assertEqual(map2.ser_data, r2.text)
        self.assertIsInstance(map1.data, list, msg='serialized content is a list of dict')
        self.assertIsInstance(map2.data, list, msg='serialized content is a list of dict')
        for d in map1.data:
            self.assertIsInstance(d, dict, msg='serialized content is a list of dict')
        for d in map2.data:
            self.assertIsInstance(d, dict, msg='serialized content is a list of dict')
        with self.assertRaises(requests.exceptions.MissingSchema):
            map1=Mapper(url='bad_url')
        with self.assertRaises(errors.WrongContent):
            sd = Mapper(url='http://localhost:8000/notexisted/').data
        with self.assertRaises(errors.WrongTrashField):
            sd = Mapper(url=url1, trash_fields='root').data


    def test_success(self):
        map1 = Mapper(url='http://localhost:8000/xmldata/', trash_fields='root.list-item')
        map2 = Mapper(url='http://localhost:8000/xmldata/', trash_fields='root')
        self.assertFalse(map1.success, msg='not success until fill')
        map1.fill_model()
        map2.fill_model()
        self.assertTrue(map1.success, msg='success if filling was successful')
        self.assertFalse(map2.success, msg='if something goes wrong')


    def test_fill_model(self):
        MapperStat_count = len(MapperStat.objects.all())
        map1 = Mapper(url='http://localhost:8000/xmldata/', trash_fields='root.list-item')
        map1.fill_model()
        map2 = Mapper(url='http://localhost:8000/jsondata/', trash_fields='root.list-item')
        map2.fill_model()
        map3 = Mapper(url='http://localhost:8000/rssdata/', trash_fields='root.list-item')
        map3.fill_model()
        self.assertEqual(len(MapperStat.objects.all()), MapperStat_count+3, msg='write information in statistic even if mapping was unsuccessful')
