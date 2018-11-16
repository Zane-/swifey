from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from .forms import LoginForm, SignupForm, ListingForm, SearchForm
from .auth import is_valid_auth

def home(request):
    authenticated = is_valid_auth(request.COOKIES)

    return render(request, 'app/index.html', {
        'authenticated': authenticated,
    })


def details(request, id):
    # make POST request to find details of listing id
    req = requests.post('http://exp-api:8000/listing/' + str(id) + '/')
    # handle valid POST request
    if req['OK']:
        return render(request, 'details.html', { 'listing': req })
    # handle invalid POST request
    else:
        # :TODO direct to future error.html page that is being created
        # for now just direct to index for no errors
        return render(request,
                                'error.html',
                                { 'err':
                                    "Listing {} doesn't exist".format(id) })

def marketplace(request):
    # make POST request to find details of all listings
    req = requests.post('http://exp-api:8000/listing/')
    # grab fields of all listings
    details_of_all = req
    return render(request, 'marketplace.html', { 'all_listings':
                                                    details_of_all })

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
                'password': form.cleaned['password']
            }
            # POST request to experience layer with data from form
            req = requests.post('http://exp-api:8000/login/',
                                    data=data)
            if req.status_code == '200':
                """ If we made it here, we can log them in. """
                response = redirect('index')
               # set the auth cookie using the json response from POST request
                response.set_cookie('auth', req.json())
                return response
        # handle invalid POST request
        else:
            # invalid form, return to login
            return render(request, 'app/form.html', {'form': form,
                                                        'err': warning})
    else:
        form = LoginForm()

    loginPage = True

    return render(request, 'app/form.html', {
         'form': form,
         'loginPage': loginPage,
         'title': 'Login',
         })


# def logout(request):
#     auth = request.COOKIES.get('auth')
#     warning = "You have entered an invalid username or password!"
#     # redirect to login page
#     if not auth:
#         return HttpResponseRedirect(reverse('login'))
#     next = HttpResponseRedirect(reverse(('login'))
#     next.delete_cookie('auth')
#     # POST logout and validate request
#     return next


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
                'have_a_meal_plan': form.cleaned_data['have_a_meal_plan'],
            }
            req = requests.post('http://exp-api:8000/signup/', data=data)
            if req.status_code == '201':
                """ If we made it here, we can sign them up. """
                response = redirect('login')
               # set the auth cookie using the json response from POST request
                response.set_cookie('auth', req.json())
                return response
        else:
            # invalid form, return to sign up
            return render(request, 'app/form.html', { 'form': form,
                                                        'err': warning })
    else:
        form = SignupForm()

    loginPage = False

    return render(request, 'app/form.html', {
         'form': form,
         'loginPage': loginPage,
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
            req = requests.post('http://exp-api:8000/new_listing/',
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

    return render(request, 'app/form.html', { 'form': form })


def search(request):
    warning = "Invalid! Please fill out all the fields appropriately."
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # handle valid POST request
        if form.is_valid():
            search = form.cleaned_data['search']
            # :TODO create api url for search
            req = requests.post('http://exp-api:8000/search/',
                                data={'query': search})
            if req.status_code == '200':
                """ If we made it here, we can redirect to search result page. """
                # :TODO req should return an array of the results back that can be referenced as req['results']
                return render(
                    request,
                    'app/search.html',
                    {'search': search, 'results': req.json(), 'form': form, 'submit': True}
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

