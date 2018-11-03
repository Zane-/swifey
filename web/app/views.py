from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests

# :TODO import UserForm, ListingForm from models/app/models.py
#   or make request via experience API?

def home(request):
    return render(request, 'app/home.html', {})

def details(request):
    for_swipes = requests.get('http://exp-api:8000/api/trades/for_swipes/').json()
    for_items = requests.get('http://exp-api:8000/api/trades/for_items/').json()
    return render(request, 'app/details.html',
        {'for_swipes': for_swipes, 'for_items': for_items})

def login(request):
    form = UserForm()
    auth = request.COOKIES.get('auth')
    warning = "You have entered an invalid username or password!"
    # Direct to home page if auth token is validated
    if auth:
        return HttpResponseRedirect(reverse('home'))
    # Return new login form
    if request.method == 'GET':
        return render(request, 'app/login.html', {'form': form, 'auth': auth, 'err': warning })
    # :TODO POST valid request
    # :TODO handle invalid POST request
    # :TODO grab auth token once post request was made successfully
    token = ''
    next = HttpResponseRedirect(reverse('home'))
    next.set_cookie('auth', token)
    return next

def logout(request):
    auth = request.COOKIES.get('auth')
    warning = "You have entered an invalid username or password!"
    if not auth:
        return HttpResponseRedirect(reverse('login'))
    # :TODO validate logout with backend
    next = HttpResponseRedirect(reverse('index'))
    next.delete_cookie('auth')
    return next

def sign_up(request):
    form = UserForm()
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all fields appropriately."
    # Direct to home page if auth token is validated
    if auth:
        return HttpResponseRedirect(reverse('index'))
    # Return new sign up form
    if request.method == 'GET':
        return render(request, 'app/sign_up.html', {'form': UserForm,'auth': auth, 'err': warning })
    # :TODO POST valid request
    # :TODO handle invalid POST request
    # :TODO grab auth token once post request was made successfully
    # :TODO handle next steps after valid POST request
    return render(request, 'app/sign_up.html', {'form': , 'auth': auth })

def new_listing(request):
    form = ListinForm()
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all fields appropriately."
    # :TODO handle new listing logic
    return render(request, 'app/new_listing.html', {'form': , 'auth': auth, 'err': warning })

