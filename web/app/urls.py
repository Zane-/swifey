from django.conf.urls import url
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('details', views.details, name='details'),
    path('login', views.login, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('new_listing', views.new_listing, name='new_listing')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
