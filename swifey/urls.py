from django.contrib import admin
from django.urls import path, include
from tastypie.api import Api
from app.resources import UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(v1_api.urls)),
]
