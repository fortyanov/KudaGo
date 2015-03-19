from django.shortcuts import render
from Main.models import SomeData
from Main.serializers import *
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class XMLResponse(HttpResponse):
    """
    An HttpResponse that renders its content into XML.
    """
    def __init__(self, data, **kwargs):
        content = XMLRenderer().render(data)
        kwargs['content_type'] = 'application/xml'
        super(XMLResponse, self).__init__(content, **kwargs)


@api_view(['GET'])
def someDataListXml(request, format=None):
    if request.method == 'GET':
        data = SomeData.objects.all()
        print("data: %s" % data)
        serializer = SomeDataSerializer(data, many=True)
        return XMLResponse(serializer.data)


@api_view(['GET', 'POST'])
def someDataListJson(request, format=None):
    if request.method == 'GET':
        data = SomeData.objects.all()
        print("data: %s" % data)
        serializer = SomeDataSerializer(data, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     print("request.data: %s" % request.data)
    #     serializer = SomeDataSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)