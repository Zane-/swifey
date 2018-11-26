from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import experience


@csrf_exempt
def get_all_listings(request):
    json = experience.get_all_listings()
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
        req = experience.signup(request.POST)
        if req == 'CREATED':
            return JsonResponse(req, status=201)
        else:
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def create_listing(request):
    if request.method == 'POST':
        resp = experience.create_listing(request.POST)
        if resp not in ('FAIL', 'AUTH ERROR'):
            return HttpResponse(resp, status=201)
        elif resp == 'AUTH ERROR':
            return HttpResponse('AUTH ERROR', status=401)
        else:
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def validate_auth(request):
    if request.method == 'POST':
        auth = {
            'user_id': request.POST.get('user_id'),
            'authenticator': request.POST.get('authenticator'),
            'date_created': request.POST.get('date_created'),
        }
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

@csrf_exempt
def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        listings = experience.search(query)
        return JsonResponse(listings, safe=False)
    else:
        return HttpResponse('Request type must be POST', status=400)
