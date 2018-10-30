from django.core.exceptions import FieldError, ValidationError
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from app.models import User, UserForm, Item

@csrf_exempt
def user_api(request, user_id=None):
    if request.method == 'GET':
        if user_id is not None:
            user = get_object_or_404(User, pk=user_id).json()
            return JsonResponse(user)
        # if a user_id wasn't passed, return all users
        else:
            users = User.objects.all()
            data = [user.json() for user in users]
            return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            # if fields are not valid, return UnprocessableEntity
            return HttpResponse(status=422)

    elif request.method == 'DELETE':
        if user_id is not None:
                get_object_or_404(User, pk=user_id).delete()
                return HttpResponse(status=202)
        # return 400 bad request if no user_id was supplied
        else:
            return HttpResponse(status=400)
    else:
        # return bad request if type wasn't GET, PUT, or DELETE
        return HttpResponse(status=400)

@csrf_exempt
def update_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse(status=202)
        else:
            # UnprocessableEntity status code
            return HttpResponse(status=422)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def item_api(request, item_id=None):
    if request.method == 'GET':
        if item_id is not None:
            item = get_object_or_404(Item, pk=item_id).json()
            return JsonResponse(item)
        # if a item_id wasn't passed, return all items
        else:
            items = Item.objects.all()
            data = [item.json() for item in items]
            return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            # if fields are not valid, return UnprocessableEntity
            return HttpResponse(status=422)

    elif request.method == 'DELETE':
        if item_id is not None:
                get_object_or_404(Item, pk=item_id).delete()
                return HttpResponse(status=202)
        # return 400 bad request if no item_id was supplied
        else:
            return HttpResponse(status=400)
    else:
        # return bad request if type wasn't GET, PUT, or DELETE
        return HttpResponse(status=400)

@csrf_exempt
def update_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)
        form = ItemForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(status=202)
        else:
            # UnprocessableEntity status code
            return HttpResponse(status=422)
    else:
        return HttpResponse(status=400)
