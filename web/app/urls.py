from django.conf.urls import url
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('create/', views.create_listing, name='create_listing'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path('search/', views.search, name='search'),
    path('profile', views.profile, name='profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
