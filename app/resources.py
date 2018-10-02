from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from app.models import User, Trade

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()

class TradeResource(ModelResource):
    class Meta: 
        queryset = Trade.objects.all() 
        resource_name = 'trade'
        authorization = Authorization() 
        excludes = ['date_created']
