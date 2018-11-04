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
    # return new login form
    if request.method == 'GET':
        return render(request, 'app/login.html', {'form': form, 'auth': auth })
    # POST valid request
    f = UserForm(request.POST)
    # handle invalid POST request
    if not f.is_valid():
        # invalid form, return to login
        return render(request, 'app/login.html', {'form': form, 'err': warning })
    # clean username and password fields
    email = f.cleaned_data['email']
    password = f.cleaned_data['password']
    # :TODO send validated information to experience layer
    response = ''
    # Experience layer checks if invalid information was provided
    if not response or not response['OK']:
        # return to login page with error message
        return render(request, 'app/login.html', { 'form': form, 'err': err })
    """ If we made it here, we can log them in. """
    # :TODO grab auth token once post request was made successfully
    # i.e. token = response['authenticator'] or whatever field
    # name is for auth token from the response
    token = ''
    next = HttpResponseRedirect(reverse('home'))
    next.set_cookie('auth', token)
    return next

def logout(request):
    auth = request.COOKIES.get('auth')
    warning = "You have entered an invalid username or password!"
    # redirect to login page
    if not auth:
        return HttpResponseRedirect(reverse('login'))
    next = HttpResponseRedirect(reverse('index'))
    next.delete_cookie('auth')
    # :TODO POST logout and validate request
    return next

def sign_up(request):
    form = UserForm()
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all fields appropriately."
    # Direct to home page if auth token is validated
    if auth:
        return HttpResponseRedirect(reverse('home'))
    # Return new sign up form
    if request.method == 'GET':
        return render(request, 'app/sign_up.html', {'form': form, 'auth': auth })
    # POST valid request
    f = UserForm(request.POST)
    # handle invalid POST request
    if not f.is_valid():
        # invalid form, return to sign_up
        return render(request, 'app/sign_up.html', { 'form': form, 'auth': auth, 'err': err })
    # clean up fields of UserForm
    first_name = f.cleaned_data['first_name']
    last_name = f.cleaned_data['last_name']
    email = f.cleaned_data['email']
    password = f.cleaned_data['password']
    university = f.cleaned_data['university']
    has_meal_plan = f.cleaned_data['has_meal_plan']
    # :TODO send validated information to experience layer
    response = ''
    # Experience layer checks if invalid information was provided
    if not response or not response['OK']:
        # return to login page with error message
        return render(request, 'app/sign_up.html', { 'form': form, 'err': err })
    next = HttpResponseRedirect(reverse('login'))
    return next

def new_listing(request):
    form = ListingForm()
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all fields appropriately."
    # redirect to login page
    if not auth:
        return HttpResponseRedirect(redirect('login') + '?next=' + reverse('new_listing'))
    # return new listing form
    if request.method == 'GET':
        return render(request, 'app/new_listing.html', { 'form': form, 'auth': auth })
    # POST valid request
    f = ListingForm(request.POST)
    # handle invalid POST request
    if not f.is_valid():
        # invalid form, return to listing form
        return render(request, 'app/new_listing.html', { 'form': form, 'auth': auth, 'err': warning })
    # clean up fields of ListingForm
    title = f.cleaned_data['title']
    description = f.cleaned_data['description']
    listing_type = f.cleaned_data['listing_type']
    num_swipes = f.cleaned_data['num_swipes']
    # :TODO send validated information to experience layer
    response = ''
    # Experience layer checks if invalid information was provided
    if not response or not response['OK']:
        # OPTIONAL :TODO check if experience layer reports invalid authenticator
        # use if statement then indent the rest
        # return to login page with error message
        return render(request, 'app/login.html', { 'form': form, 'err': err })
    """ If we made it here, we have succesfully created listing. """
    return HttpResponseRedirect(reverse('index'))
