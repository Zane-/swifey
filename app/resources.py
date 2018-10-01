from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from app.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
