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
        if req != 'FAIL':
            return JsonResponse(req, status=200)
        else:
            return HttpResponse('FAIL', status=401)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        signup = experience.signup(request.POST)
        if signup == 'CREATED':
            return JsonResponse(req, status=201)
        else:
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def create_listing(request):
    if request.method == 'POST':
        create = experience.create_listing(request.POST)
        if create == 'OK':
            return HttpResponse('OK', status=201)
        elif create == 'AUTH ERROR':
            return HttpResponse('AUTH ERROR', status=201)
        else:
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def validate_auth(request):
    if reqeust.method == 'POST':
        auth = request.POST.get('auth')
        valid = experience.validate_auth(auth)
        if valid:
            return HttpResponse('OK', status=200)
        else:
            return HttpResponse('FAIL', status=401)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        valid = experience.validate_email(email)
        if valid:
            return HttpResponse('OK', status=200)
        else:
            return HttpResponse('FAIL', status=409)
    else:
        return HttpResponse('Request type must be POST', status=400)
