from django.test import TestCase
from .models import Authenticator, User, UserForm, Listing, ListingForm

import json
import hmac
from datetime import date

#:TODO Bugi will write the test cases after we have finished our
# front-end so he can make valid requests using self.client()

# class UserTestCase(TestCase):
#     def setUp(self):
#         user = User.objects.create(
#                 first_name='bugi',
#                 last_name='king',
#                 email='bugi@virginia.edu',
#                 university='University of Virginia',
#                 has_meal_plan=false,
#                 date_joined=date.today,
#                 listings=''
#         )
#
#     def test_get_listings(self):
#
#     def test_set_listings(self):
#
#     def test_json(self):
#
# class UserFormTestCase(TestCase):
#     def setUp(self):
#         pass
#
# class ListingTestCase(TestCase):
#     def setUp(self):
#         listing = Listing.objects.create(
#                     title='',
#                     description='',
#                     user_id=1,
#                     listing_type='S',
#                     num_swipes=5,
#                     last_modified=date.today,
#         )
#
#     def test_json(self):
#
# class ListingFormTestCase(TestCase):
#     def setUp(self):
#         pass
#
