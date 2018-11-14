from django.conf.urls import url
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('details/', views.details, name='details'),
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='sign_up'),
    path('create/', views.create_listing, name='create_listing')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
