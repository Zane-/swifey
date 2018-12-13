import ast
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .forms import LoginForm, SignupForm, ListingForm, SearchForm
from .auth import is_valid_auth

def index(request):
    authenticated = is_valid_auth(request.COOKIES)
    return render(
        request,
        'app/index.html',
        {'authenticated': authenticated}
    )

def marketplace(request):
    # :TODO
    # - Add a filter button that passes a post variable
    # to the template to determine what to show
    # - Add a search bar, this should just get results
    # and render them to the marketplace template

    req = requests.get('http://exp-api:8000/api/listing/')
    authenticated = is_valid_auth(request.COOKIES)
    # grab fields of all listings
    listings = req.json()
    return render(
        request,
        'app/marketplace.html',
        {'listings': listings, 'authenticated': authenticated}
    )

def login(request):
    warning = "You have entered an invalid username or password!"

    authenticated = is_valid_auth(request.COOKIES)
    # Direct to home page if auth token is validated
    if authenticated:
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

    return render(
        request,
        'app/form.html',
        {'form': form, 'title': 'Log in',}
    )


def logout(request):
    auth = request.COOKIES.get('auth')
    resp = redirect('login')
    resp.delete_cookie('auth')
    return resp


def sign_up(request):
    warning = "Invalid! Please fill out all the fields appropriately."

    # Direct to home page if auth token is validated
    authenticated = is_valid_auth(request.COOKIES)
    if authenticated:
        return redirect('index')

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
            if req.status_code == 201:
                response = redirect('index')
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

    return render(
        request,
        'app/form.html',
        {'form': form,'title': 'Sign Up',}
    )


def create_listing(request):
    warning = "Invalid! Please fill out all the fields appropriately."

    authenticated = is_valid_auth(request.COOKIES)
    # Direct to login page if auth token is not validated
    if not authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ListingForm(request.POST)
        # handle valid POST request
        auth = ast.literal_eval(request.COOKIES.get('auth'))
        if form.is_valid():
            data= {
                'authenticator': auth['authenticator'],
                'user_id': auth['user_id'],
                'auth_date_created': auth['date_created'],
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'listing_type': form.cleaned_data['listing_type'],
                'num_swipes': form.cleaned_data['num_swipes'],
            }

            req = requests.post('http://exp-api:8000/api/create_listing/', data=data)
            if req.status_code == 201:
                # the id of the listing is returned from the post request
                response = redirect('/listing/{}/'.format(req.text))
                return response
        else:
            # invalid form, return to new listing
            return render(
                request,
                'app/form.html',
                {'form': form,'err': warning}
            )
    else:
        form = ListingForm()

    return render(
        request,
        'app/form.html',
        {'form': form, 'authenticated': authenticated}
    )


def listing(request, listing_id):
    authenticated = is_valid_auth(request.COOKIES)
    user_id = ast.literal_eval(request.COOKIES.get('auth'))['user_id']
    # post user_id and listing_id to experience to push to kafka
    rec_push = requests.post('http://exp-api:8000/api/recommendations/', data={'user_id': user_id, 'listing_id': listing_id})

    rec_pull = requests.get('http://exp-api:8000/api/recommendations/{}'.format(listing_id))
    if rec_pull.status_code == 200:
        recs = rec_pull.json()
    else:
        recs = []

    req = requests.get('http://exp-api:8000/api/listing/{}/'.format(listing_id))
    if req.status_code == 404:
        return HttpResponse(status=404)

    listing = req.json()

    return render(
        request,
        'app/listing.html',
        {'listing': listing, 'authenticated': authenticated, 'recommendations': recs}
    )

def profile(request):
    authenticated = is_valid_auth(request.COOKIES)
    if not authenticated:
        return redirect('login')

    # extract user_id from cookie to render info
    user_id = ast.literal_eval(request.COOKIES.get('auth'))['user_id']
    return render(
        request,
        'app/profile.html',
        {'user_id': user_id, 'authenticated': authenticated}
    )


def search(request):
    warning = "Invalid! Please fill out all the fields appropriately."
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # handle valid POST request
        if form.is_valid():
            data = {'query': form.cleaned_data['search']}
            req = requests.post('http://exp-api:8000/api/search/', data=data)
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

