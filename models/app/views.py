from django.contrib.auth.hashers import check_password
from django.core.exceptions import FieldError, ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from app.models import Authenticator, User, UserForm, Listing, ListingForm

@csrf_exempt
def model_api(request, model, model_form, pk=None):
    if request.method == 'GET':
        if pk is not None:
            obj = get_object_or_404(model, pk=pk).json()
            return JsonResponse(obj)
        # if a pk wasn't passed, return all objects
        else:
            objs = model.objects.all()
            data = [obj.json() for obj in objs]
            return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        form = model_form(request.POST)
        if form.is_valid():
            # return object id to index in ES
            f = form.save()
            return HttpResponse(f.pk, status=201)
        else:
            # if fields are not valid, return UnprocessableEntity
            return HttpResponse('UnprocessableEntity', status=422)

    elif request.method == 'DELETE':
        if pk is not None:
                get_object_or_404(model, pk=pk).delete()
                return HttpResponse('OK', status=202)
        # return 400 bad request if no pk was supplied
        else:
            return HttpResponse('Must supply object id', status=400)
    else:
        # return bad request if type wasn't GET, PUT, or DELETE
        return HttpResponse('Bad request type', status=400)


@csrf_exempt
def update_model(request, model, model_form, pk):
    if request.method == 'POST':
        obj = get_object_or_404(model, pk=pk)
        form = model_form(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('OK', status=202)
        else:
            # UnprocessableEntity status code
            return HttpResponse('UnprocessableEntity', status=422)
    else:
        return HttpResponse('Bad request type', status=400)


@csrf_exempt
def user_api(request, user_id=None):
    return model_api(request, User, UserForm, user_id)

@csrf_exempt
def update_user(request, user_id=None):
    return update_model(request, User, UserForm, user_id)

@csrf_exempt
def listing_api(request, listing_id=None):
    return model_api(request, Listing, ListingForm, listing_id)

@csrf_exempt
def update_listing(request, listing_id=None):
    return update_model(request, Listing, ListingForm, listing_id)


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except ObjectDoesNotExist:
            return HttpResponse('FAIL', status=401)

        if user:
            password = request.POST.get('password')
            login = check_password(password, user.password)
            if login:
                auth = Authenticator.objects.create(user_id=user.id)
                auth.save()
                return JsonResponse(auth.json())
        # either bad password or user does not exist
        return HttpResponse('FAIL', status=401)

    else:
        return HttpResponse('Request type must be POST', status=400)


@csrf_exempt
def validate_auth(request):
    if request.method == 'POST':
        try:
            auth = Authenticator.objects.get(pk=request.POST.get('authenticator'))
        except ObjectDoesNotExist:
            return HttpResponse('FAIL', status=404)
        # this will be passed in from the auth object stored in the user's cookie
        user_id = request.POST.get('user_id')
        if int(auth.user_id) == int(user_id) and not auth.is_expired():
            return HttpResponse('OK', status=200)
        else:
            if auth.is_expired():
                auth.delete()
            return HttpResponse('FAIL', status=401)

    else:
        return HttpResponse('Request type must be POST', status=400)


@csrf_exempt
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return HttpResponse('OK', status=200)
        else:
            return HttpResponse('FAIL', status=409)
    else:
        return HttpResponse('Request type must be POST', status=400)

