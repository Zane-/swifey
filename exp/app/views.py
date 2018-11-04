from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import experience


@csrf_exempt
def get_listings(request, listing_type=None, sort=None):
    if listing_type is None:
        json = experience.get_all('listing')
        return JsonResponse(json, safe=False)

    json = experience.get_listings(listing_type=listing_type, sort=sort)
    return JsonResponse(json, safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        req = experience.login(request.POST)
        if req == 'SUCCESS':
            return HttpResponse('SUCCESS', status=200)
        else:
            return HttpResponse('FAIL', status=401)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        signup = experience.signup(request.POST)
        if signup == 'CREATED':
            return HttpResponse('CREATED', status=201)
        else:
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Request type must be POST', status=400)

def create_listing(request):
    pass


