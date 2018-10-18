from django.urls import path

from . import views

urlpatterns = [
    path(
        'trades/for_swipes/',
        views.for_swipe_trades,
        name='for_swipe_trades'
    ),
    path(
        'trades/for_swipes/sorted_high/',
        views.for_swipe_trades_sorted_high,
        name='for_swipe_trades_sorted_high'
    ),
    path(
        'trades/for_swipes/sorted_low/',
        views.for_swipe_trades_sorted_low,
        name='for_swipe_trades_sorted_low'
    ),
    path(
        'trades/for_items/',
        views.for_item_trades,
        name='index'
    ),
    path(
        'trades/for_items/sorted_high/',
        views.for_item_trades_sorted_high,
        name='index'
    ),
    path(
        'trades/for_items/sorted_low/',
        views.for_item_trades_sorted_low,
        name='index'
    ),
]
