from django.test import TestCase
from django.urls import reverse

import json
import hmac
from datetime import date


from .models import Authenticator, User, UserForm, Listing, ListingForm

#:TODO Bugi will write the test cases after we have finished our
# front-end so he can make valid requests using self.client()

class UserViewTest(TestCase):
    def setUp(self):
        pass

    def test_user_url(self):
        resp = self.client.get(reverse('users'))
        self.assertEqual(resp.status_code, 200)

class UserCreateTest(TestCase):
    def setUp(self):
        user = User.objects.create(
                first_name='bugi',
                last_name='king',
                email='bugi@virginia.edu',
                university='University of Virginia',
                has_meal_plan=False,
                date_joined=date.today,
                listings='2 meal swipes'
        )

    def test_user_first_name(self):
        resp = User.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_first_name = ''.join(resp.first_name)
        self.assertEqual(expected_first_name, 'bugi')

    # def test_user_last_name(self):
    #     resp = User.objects.get(pk=1)
    #     # f-strings not available in Python 3.5.4
    #     expected_last_name = ''.join(resp['last_name'])
    #     self.assertEqual(expected_last_name, 'king')
    #
    # def test_user_email(self):
    #     resp = User.objects.get(pk=1)
    #     # f-strings not available in Python 3.5.4
    #     expected_email = ''.join(resp.email)
    #     self.assertEqual(expected_email, 'bugi@virginia.edu')
    #
    # def test_user_university(self):
    #     resp = User.objects.get(pk=1)
    #     # f-strings not available in Python 3.5.4
    #     expected_university = ''.join(resp.university)
    #     self.assertEqual(expected_university, 'University of Virginia')
    #
    # def test_user_mealplan(self):
    #     resp = User.objects.get(pk=1)
    #     expected_mealplan = resp.has_meal_plan
    #     self.assertEqual(expected_mealplan, False)
    #
    # # def test_user_date_joined(self):
    # #     resp = User.objects.get(pk=1)
    # #     expected_date = resp.date_joined
    # #     self.assertEqual(expected_date, date.today)
    #
    # def test_user_listing(self):
    #     resp = User.objecs.get(pk=1)
    #     # f-strings not available in Python 3.5.4
    #     expected_listing = ''.join(resp.listings)
    #     self.assertEqual(expected_listing, '2 meal swipes')
    #
class ListingViewTest(TestCase):
    def setUp(self):
        pass

    def test_listing_url(self):
        resp = self.client.get(reverse('listings'))
        self.assertEqual(resp.status_code, 200)

class ListingCreatetTest(TestCase):
    def setUp(self):
        listing = Listing.objects.create(
                    title='2 swipes',
                    description='swipes for hw',
                    user_id=1,
                    listing_type='S',
                    num_swipes=5,
                    last_modified=date.today,
        )

    def test_listing_title(self):
        resp = Listing.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_title = ''.join(resp.title)
        self.assertEqual(expected_title, '2 swipes')
