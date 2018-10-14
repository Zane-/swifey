from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from app.models import User, Item

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()

class ItemResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        authorization = Authorization()
        excludes = ['date_created']
