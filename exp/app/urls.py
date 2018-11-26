from django.urls import path

from . import views

urlpatterns = [
    path('listing/', views.get_all_listings, name='all_listings'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('validate_auth/', views.validate_auth, name='validate_auth'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('search/', views.search, name='search'),
]
