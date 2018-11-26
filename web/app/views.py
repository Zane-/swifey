import ast
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import LoginForm, SignupForm, ListingForm, SearchForm
from .auth import is_valid_auth

def index(request):
    auth = request.COOKIES.get('auth')
    # takes the string representing the dict and converts it to a dict
    auth = ast.literal_eval(auth)
    authenticated = is_valid_auth(auth)
    return render(
        request,
        'app/index.html',
        {'login': authenticated}
    )

def marketplace(request):
    # make POST request to find details of all listings
    req = requests.post('http://exp-api:8000/api/listing/')
    # grab fields of all listings
    listings = req.json()
    return render(
        request,
        'marketplace.html',
        {'listings': listings}
    )

def login(request):
    auth = request.COOKIES.get('auth')
    warning = "You have entered an invalid username or password!"
    # Direct to home page if auth token is validated
    if auth:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # handle valid POST request
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }
            # POST request to experience layer with data from form
            req = requests.post('http://exp-api:8000/api/login/', data=data)
            if req.status_code == 200:
                resp = redirect('index')
                # set the auth cookie using the json response from POST request
                resp.set_cookie('auth', req.json())
                return resp
        # handle invalid POST request
        else:
            # invalid form, return to login
            return render(
                request,
                'app/form.html',
                {'form': form, 'err': warning}
            )
    else:
        form = LoginForm()

    loginPage = True
    return render(request, 'app/form.html', {
         'form': form,
         'title': 'Login',
    })


def logout(request):
    auth = request.COOKIES.get('auth')
    resp = redirect('login')
    resp.delete_cookie('auth')
    return resp


def sign_up(request):
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all the fields appropriately."
    # Direct to home page if auth token is validated
    if auth:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # handle valid POST request
        if form.is_valid():
            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'university': form.cleaned_data['university'],
                'has_meal_plan': form.cleaned_data['have_a_meal_plan'],
            }
            req = requests.post('http://exp-api:8000/api/signup/', data=data)
            if req.status_code == '201':
                response = redirect('/')
                response.set_cookie('auth', req.json(), max_age=604800)
               # set the auth cookie using the json response from POST request
                return response
        else:
            # invalid form, return to sign up
            return render(
                request,
                'app/form.html',
                {'form': form, 'err': warning}
            )
    else:
        form = SignupForm()

    return render(request, 'app/form.html', {
         'form': form,
         'title': 'Sign Up',
    })


def create_listing(request):
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all the fields appropriately."
    # Direct to login page if auth token is not validated
    if not auth:
        return redirect('login')
    if request.method == 'POST':
        form = ListingForm(request.POST)
        # handle valid POST request
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'listing_type': form.cleaned_data['listing_type'],
                'num_swipes': form.cleaned_data['num_swipes'],
            }
            req = requests.post('http://exp-api:8000/api/new_listing/',
                                    data=data)
            if req.status_code == '201':
                """ If we made it here, we can create new listing. """
                response = redirect('index')
                return response
        else:
            # invalid form, return to new listing
            return render(request,
                            'app/new_listing.html',
                            { 'form': form,
                                'err': warning })
    else:
        form = ListingForm()

    return render(request, 'app/form.html', {'form': form})


def profile(request):
    auth = requests.COOKIES.get('auth')
    auth = ast.literal_eval(auth)
    authenticated = is_valid_auth(auth)
    if not authenticated:
        return redirect('login')
    user_id = auth['user_id']
    # populate template based on info obtained from user_id passed in
    return render(request, 'app/profile.html', {'user_id': user_id})


def search(request):
    warning = "Invalid! Please fill out all the fields appropriately."
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # handle valid POST request
        if form.is_valid():
            search = form.cleaned_data['search']
            req = requests.post('http://exp-api:8000/api/search/',
                                data={'query': search})
            return render(
                request,
                'app/search.html',
                {'search': search, 'results': req.json(), 'submit': True}
            )
        else:
            # invalid form
            # :TODO create search.html that has a search bar
            return render(
                request,
                'app/search.html',
                {'form': form, 'err': warning}
            )
    else:
        form = SearchForm()

    return render(request, 'app/form.html', {'form': form})

