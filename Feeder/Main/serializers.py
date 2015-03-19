from rest_framework.serializers import *
from Main.models import *


class SomeDataSerializer(ModelSerializer):
    class Meta:
        model = SomeData
        fields = ('id', 'title', 'link', 'description', 'author', 'category', 'comments', 'pubDate', 'placement')
        #fields = ('id', 'title', 'link', 'description')

