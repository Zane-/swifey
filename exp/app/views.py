from django.shortcuts import render
from django.http import JsonResponse

from . import experience

def for_swipe_listings(request):
    json = experience.get_listings(for_swipes=True)
    return JsonResponse(json, safe=False)

def for_swipe_listings_sorted_low(request):
    json = experience.get_listings(for_swipes=True, sort='low')
    return JsonResponse(json, safe=False)

def for_swipe_listings_sorted_high(request):
    json = experience.get_listings(for_swipes=True, sort='high')
    return JsonResponse(json, safe=False)

def for_item_listings(request):
    json = experience.get_listings(for_swipes=False)
    return JsonResponse(json, safe=False)

def for_item_listings_sorted_low(request):
    json = experience.get_listings(for_swipes=False, sort='low')
    return JsonResponse(json, safe=False)

def for_item_listings_sorted_high(request):
    json = experience.get_listings(for_swipes=False, sort='high')
    return JsonResponse(json, safe=False)
