import datetime
import hmac
import json
import os

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email, RegexValidator
from django.db import models
from django.forms import ModelForm, PasswordInput


class Authenticator(models.Model):
    user_id = models.IntegerField()
    authenticator = models.CharField(max_length=64, primary_key=True)
    date_created = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        """Overrides the save method to set the auth token."""
        self.authenticator = self.generate_auth()
        super(Authenticator, self).save(*args, **kwargs)

    def generate_auth(self):
        """Generates a 256 bit random authentication bitstring."""
        auth = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        # if auth is already in the db, recurse and generate a new one
        if self.auth_exists(auth):
            self.generate_auth()
        else:
            return auth

    def auth_exists(self, auth):
        """
        Checks if a generated auth token already exists in the database.
        """
        return Authenticator.objects.filter(pk=auth).exists()

    def is_expired(self):
        """
        Checks if an auth token is expired (more than a week old)
        """
        date = datetime.date.today()
        delta = date - self.date_created
        return delta.days > 7

    def json(self):
        return {
            "user_id": self.user_id,
            "authenticator": self.authenticator,
            "date_created": self.date_created,
        }


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    university = models.CharField(max_length=100)
    has_meal_plan = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Overrides the save method to hash password."""
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def json(self):
        """Returns a python dictionary of field values."""
        return {
            'id': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'university': self.university,
            'has_meal_plan': self.has_meal_plan,
            'date_joined': self.date_joined,
        }

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'university',
            'has_meal_plan',
        ]
        widgets = {
                'password': PasswordInput(),
        }


class Listing(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    user_id = models.IntegerField()
    # listing type is what is being traded
    listing_type = models.CharField(
        max_length=1,
        choices=(('S', 'Swipe'), ('M', 'Meal Exchange'), ('I', 'Item'))
    )
    num_swipes = models.IntegerField()
    last_modified = models.DateField(auto_now=True)

    def json(self):
        """Returns a python dictionary of field values."""
        return {
            'id': self.pk,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'listing_type': self.listing_type,
            'num_swipes': self.num_swipes,
            'last_modified': self.last_modified,
        }

    def __str__(self):
        return self.title


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'listing_type',
            'num_swipes',
            'user_id'
        ]

