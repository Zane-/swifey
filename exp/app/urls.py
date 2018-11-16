from django.urls import path

from . import views

urlpatterns = [
    path('listing/', views.get_listings, name='all_listings'),
    path('listing/<slug:listing_type>/', views.get_listings, name='get_listing_type'),
    path('listing/<slug:listing_type>/<slug:sort>/', views.get_listings, name='get_listing_type_sorted'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('new_listing/', views.create_listing, name='create_listing'),
    path('validate_auth/', views.validate_auth, name='validate_auth'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('search/', views.search, name='search'),
]
