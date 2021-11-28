from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from django.conf import settings
import requests
import json
from rest_framework_xml.renderers import XMLRenderer
from django.http import JsonResponse

# Create your views here.

API_KEY = settings.API_KEY


@api_view(['POST'])
def address(request):
    '''Checking for method'''
    output = {}
    coordinates = {}
    if request.method == "POST":
        '''
        loading data from json input
        then taking individual values of address and output_format
        '''
        json_data = json.loads(request.body)
        if json_data:
            address = json_data['address']
            # this line will replace # with null
            replaced = address.replace('#', '')
            output_format = json_data['output_format']

            # hiting url goes here and return response to res
            url = f'https://maps.googleapis.com/maps/api/geocode/json?address={replaced}&key={API_KEY}'
            res = requests.get(url)
            # converting res to json
            res_dict = res.json()

            # making coordinates dictionary for final dictionary
            coordinates["lat"] = res_dict['results'][0]['geometry']['location']['lat']
            coordinates["lng"] = res_dict['results'][0]['geometry']['location']['lng']

            # appending coordinates dictionary and address to otuput dictionary
            output['coordinates'] = coordinates
            output['address'] = address
    '''
    will check for output format and return appropriate return method
    in this case the default output will xml added in settings.py 
    '''
    if output_format == "json":
        return JsonResponse(output)
    elif output_format == "xml":
        return Response(output)
    else:
        return Response("Format only json or xml")

