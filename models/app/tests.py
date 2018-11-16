from django.test import TestCase
from django.urls import reverse

import json
import hmac
from datetime import date


from .models import Authenticator, User, UserForm, Listing, ListingForm

#:TODO Bugi will write the test cases after we have finished our
# front-end so he can make valid requests using self.client()

class UserViewTest(TestCase):
    fixtures = ['db_init.json']

    def setUp(self):
        pass

    def test_user_url(self):
        resp = self.client.get(reverse('users'))
        self.assertEqual(resp.status_code, 200)

class UserCreateTest(TestCase):
    fixtures = ['db_init.json']

    def setUp(self):
        pass

    def test_user_first_name(self):
        resp = User.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_first_name = ''.join(resp.first_name)
        self.assertEqual(expected_first_name, 'Bugi')

    def test_user_last_name(self):
        resp = User.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_last_name = ''.join(resp.last_name)
        self.assertEqual(expected_last_name, 'King')

    def test_user_email(self):
        resp = User.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_email = ''.join(resp.email)
        self.assertEqual(expected_email, 'bugi@email.com')

    def test_user_university(self):
        resp = User.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_university = ''.join(resp.university)
        self.assertEqual(expected_university, 'University of Virginia')

    def test_user_mealplan(self):
        resp = User.objects.get(pk=1)
        expected_mealplan = resp.has_meal_plan
        self.assertEqual(expected_mealplan, False)

    def test_user_date_joined(self):
        resp = User.objects.get(pk=1)
        expected_date = resp.date_joined
        self.assertEqual(str(expected_date), '2018-10-29')

    def test_user_listing(self):
        resp = User.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_listing = ''.join(resp.listings)
        self.assertEqual(expected_listing, 'rich')

class ListingViewTest(TestCase):
    fixtures = ['db_init.json']

    def setUp(self):
        pass

    def test_listing_url(self):
        resp = self.client.get(reverse('listings'))
        self.assertEqual(resp.status_code, 200)

class ListingCreatetTest(TestCase):
    fixtures = ['db_init.json']

    def setUp(self):
        pass

    def test_listing_title(self):
        resp = Listing.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_title = ''.join(resp.title)
        self.assertEqual(expected_title, 'need to survive')

    def test_listing_description(self):
        resp = Listing.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_description = ''.join(resp.description)
        self.assertEqual(expected_description, 'Looking for a new swifey')


    def test_listing_user_id(self):
        resp = Listing.objects.get(pk=1)
        expected_user_id = resp.user_id
        self.assertEqual(expected_user_id, 1)


    def test_listing_type(self):
        resp = Listing.objects.get(pk=1)
        # f-strings not available in Python 3.5.4
        expected_type = ''.join(resp.listing_type)
        self.assertEqual(expected_type, 'I')


    def test_listing_num_swipes(self):
        resp = Listing.objects.get(pk=1)
        expected_num_swipes = resp.num_swipes
        self.assertEqual(expected_num_swipes, 2 )


    def test_listing_last_modified(self):
        resp = Listing.objects.get(pk=1)
        expected_date = resp.last_modified
        self.assertEqual(expected_date, date(2018, 10, 30))

class AuthenticatorCreateTest(TestCase):
    fixtures = ['db_init.json']

    def test_auth_userid(self):
        resp = Authenticator.objects.get(authenticator=111)
        expected_userid = resp.user_id
        self.assertEqual(expected_userid, 3)

    def test_auth_token(self):
        resp = Authenticator.objects.get(authenticator=111)
        expected_token = resp.authenticator
        self.assertEqual(expected_token, "111")

    def test_auth_date(self):
        resp = Authenticator.objects.get(authenticator=111)
        expected_date = resp.date_created
        self.assertEqual(expected_date, date(2018, 10, 31))

