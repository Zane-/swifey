from django.shortcuts import render
from django.http import HttpResponse
import requests

def home(request):
    return render(request, 'app/home.html', {})

def details(request):
    for_swipes = requests.get('http://exp-api:8000/api/trades/for_swipes/').json()
    for_items = requests.get('http://exp-api:8000/api/trades/for_items/').json()
    return render(request, 'app/details.html',
        {'for_swipes': for_swipes, 'for_items': for_items})
