from django.urls import path

from . import views

urlpatterns = [
    path(
        'listings/for_swipes/',
        views.for_swipe_listings,
        name='for_swipe_listings'
    ),
    path(
        'listings/for_swipes/sorted_high/',
        views.for_swipe_listings_sorted_high,
        name='for_swipe_listings_sorted_high'
    ),
    path(
        'listings/for_swipes/sorted_low/',
        views.for_swipe_listings_sorted_low,
        name='for_swipe_listings_sorted_low'
    ),
    path(
        'listings/for_items/',
        views.for_item_listings,
        name='index'
    ),
    path(
        'listings/for_items/sorted_high/',
        views.for_item_listings_sorted_high,
        name='index'
    ),
    path(
        'listings/for_items/sorted_low/',
        views.for_item_listings_sorted_low,
        name='index'
    ),
]
