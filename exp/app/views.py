from django.shortcuts import render
from django.http import JsonResponse

from . import experience


def get_listings(request, listing_type=None, sort=None):
    if listing_type is None:
        json = experience.get_all('listing')
        return JsonResponse(json, safe=False)

    json = experience.get_listings(listing_type=listing_type, sort=sort)
    return JsonResponse(json, safe=False)
