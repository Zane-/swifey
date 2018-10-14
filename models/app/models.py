from django.db import models
from datetime import datetime
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    seller_status = models.BooleanField(default=True)
    email = models.CharField(max_length=30)
    university = models.CharField(max_length=100)

class Item(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    num_swipes = models.IntegerField()
    created_by = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.now, blank=True)

