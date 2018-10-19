from django.shortcuts import render
#import requests
def home(request):

    return render(request, 'app/home.html', {

    })

def details(request):
    #json = requests.get('http://exp-api:8000/trades/for_swipes/').json()
    return render(request, 'app/details.html', {
        #'json': json, 
    })