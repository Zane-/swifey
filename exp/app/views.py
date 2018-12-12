from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import HTTPError

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
        if req != 'FAIL' :
            return JsonResponse(req, status=201)
        else:
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Request type must be POST', status=400)

@csrf_exempt
def get_listing(request, listing_id):
    if request.method == 'GET':
        try:
            json = experience.get('listing', listing_id)
        except HTTPError:
            return HttpResponse('Listing does not exist', status=404)
        return JsonResponse(json, status=200)
    else:
        return HttpResponse('Request type must be GET', status=400)

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
        valid = experience.validate_email(request.POST)
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

@csrf_exempt
def recommendations(request, listing_id=None):
    if request.method == 'GET':
        if listing_id is None:
            return HttpResponse(status=400)
        rec = experience.get_recommendations(listing_id)
        if rec != 'FAIL':
            return JsonResponse(rec, safe=False)
        else:
            return HttpResponse(status=404)
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        listing_id = request.POST.get('listing_id')
        if user_id is None or listing_id is None:
            return HttpResponse(status=400)
        experience.push_recommendation(user_id, listing_id)
        return HttpResponse(status=200)
    else:
        return HttpResponse('Request type must be GET or POST', status=400)
