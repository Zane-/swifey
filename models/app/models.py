from datetime import datetime
from django.db import models
from django.forms import ModelForm

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    seller_status = models.BooleanField(default=True)
    email = models.CharField(max_length=30)
    university = models.CharField(max_length=100)

    def json(self):
        return {
            'id': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'seller_status': self.seller_status,
            'email': self.email,
            'university': self.university
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class Item(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    num_swipes = models.IntegerField()
    created_by = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    label = models.CharField(max_length=1)
    for_swipes = models.BooleanField(default=True)

    def json(self):
        return {
            'title': self.title,
            'description': self.description,
            'num_swipes': self.num_swipes,
            'created_by': self.created_by,
            'date_created': self.date_created,
            'label': self.label,
            'for_swipes': self.for_swipes
        }

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
