from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.user_api, name='users'),
    path('user/<int:user_id>/', views.user_api, name='user_api'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('item/', views.item_api, name='items'),
    path('item/<int:item_id>/', views.item_api, name='item_api'),
    path('item/<int:item_id>/update/', views.update_item, name='update_item'),
]
