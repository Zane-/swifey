from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    seller_status = models.BooleanField(default=True)
    email = models.CharField(max_length=30)
    university = models.CharField(max_length=100)
