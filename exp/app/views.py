from django.shortcuts import render
from django.http import JsonResponse

from . import experience

def for_swipe_trades(request):
    json = experience.get_trades(for_swipes=True)
    return JsonResponse(json, safe=False)

def for_swipe_trades_sorted_low(request):
    json = experience.get_trades(for_swipes=True, sort='low')
    return JsonResponse(json, safe=False)

def for_swipe_trades_sorted_high(request):
    json = experience.get_trades(for_swipes=True, sort='high')
    return JsonResponse(json, safe=False)

def for_item_trades(request):
    json = experience.get_trades(for_swipes=False)
    return JsonResponse(json, safe=False)

def for_item_trades_sorted_low(request):
    json = experience.get_trades(for_swipes=False, sort='low')
    return JsonResponse(json, safe=False)

def for_item_trades_sorted_high(request):
    json = experience.get_trades(for_swipes=False, sort='high')
    return JsonResponse(json, safe=False)
