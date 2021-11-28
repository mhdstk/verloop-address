from django.conf import urls
from django.urls import path
from core.views import *

urlpatterns=[
    path('getAddressDetails/',address)
]
