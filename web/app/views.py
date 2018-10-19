from django.shortcuts import render
from django.http import HttpResponse
import requests

def home(request):
    return render(request, 'app/home.html', {})

def details(request):
    json = requests.get('http://exp-api:8000/api/trades/for_swipes/')
    return HttpResponse(json)
    return render(request, 'app/details.html', {'json': json})
