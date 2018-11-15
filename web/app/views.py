from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from .forms import LoginForm, SignupForm, ListingForm

def home(request):
    return render(request, 'app/index.html', {})


def details(request):
    pass

def login(request):
    auth = request.COOKIES.get('auth')
    warning = "You have entered an invalid username or password!"
    # Direct to home page if auth token is validated
    if auth:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = Login(request.POST)
        # handle valid POST request
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'password': form.cleaned['password']
            }
            # POST request to experience layer with data from form
            req = requests.post('http://exp-api:8000/login/', data=data)
            if req.status_code == '200':
                """ If we made it here, we can log them in. """
                response = HttpResponseRedirect(reverse('index'))
               # set the auth cookie using the json response from POST request
                response.set_cookie('auth', req.json())
                return response
        # handle invalid POST request
        else:
            # invalid form, return to login
            return render(request, 'app/login.html', {'form': form, 'err': warning})
    else:
        form = LoginForm()

    return render(request, 'app/form.html', { 'form': form })


def logout(request):
    auth = request.COOKIES.get('auth')
    warning = "You have entered an invalid username or password!"
    # redirect to login page
    if not auth:
        return HttpResponseRedirect(reverse('login'))
    next = HttpResponseRedirect(reverse('login'))
    next.delete_cookie('auth')
    # POST logout and validate request
    return next


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
                'has_meal_plan': form.cleaned_data['has_meal_plan'],
            }
            req = requests.post('http://exp-api:8000/signup/', data=data)
            if req.status_code == '201':
                """ If we made it here, we can sign them up. """
                response = HttpResponseRedirect(redirect('login'))
               # set the auth cookie using the json response from POST request
                response.set_cookie('auth', req.json())
                return response
        else:
            # invalid form, return to sign up
            return render(request, 'app/signup.html', { 'form': form, 'err': warning })
    else:
        form = SignupForm()

    return render(request, 'app/form.html', { 'form': form })


def create_listing(request):
    auth = request.COOKIES.get('auth')
    warning = "Invalid! Please fill out all the fields appropriately."
    # Direct to login page if auth token is not validated
    if not auth:
        return HttpResponseRedirect(redirect('login'))
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
            req = requests.post('http://exp-api:8000/new_listing/', data=data)
            if req.status_code == '201':
                """ If we made it here, we can create new listing. """
                response = HttpResponseRedirect(redirect('index'))
                return response
        else:
            # invalid form, return to new listing
            return render(request, 'app/new_listing.html', { 'form': form, 'err': warning })
    else:
        form = ListingForm()

    return render(request, 'app/form.html', { 'form': form })

#
# def search(request):
#     auth = request.COOKIES.get('auth')
#     # warning = "Invalid! Please fill out all the fields appropriately."
#     # Direct to login page if auth token is not validated
#     if not auth:
#         return HttpResponseRedirect(redirect('login'))
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         # handle valid POST request
#         if form.is_valid():
#             data = {
#                 'search': form.cleaned_data['search'],
#             }
#             url for search doesn't exist yet
#             req = requests.post('http://exp-api:8000/new_listing/', data=data)
#             if req.status_code == '200':
#                 """ If we made it here, we can redirect to search result page. """
#                 response = HttpResponseRedirect(redirect('index'))
#                 return response
#         else:
#             # invalid form
#             return render(request, 'app/new_listing.html', { 'form': form, 'err': warning })
#     else:
#         form = ListingForm()
#
#     return render(request, 'app/form.html', { 'form': form })
