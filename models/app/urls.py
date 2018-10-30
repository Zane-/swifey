from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.user_api, name='users'),
    path('user/<int:user_id>/', views.user_api, name='user_api'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('listing/', views.listing_api, name='listings'),
    path('listing/<int:listing_id>/', views.listing_api, name='listing_api'),
    path('listing/<int:listing_id>/update/', views.update_listing, name='update_listing'),
]