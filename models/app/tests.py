from datetime import date

from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from .models import Authenticator, User, Listing


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            first_name='Test',
            last_name='Testington',
            email='test@gmail.com',
            password='testpassword123',
            has_meal_plan=True,
            university='UVA',
        )

    def test_password_hash(self):
        user = User.objects.get(first_name='Test')
        # the password should have been hashed
        self.assertNotEqual(user.password, 'testpassword123')

    def test_password_check(self):
        user = User.objects.get(first_name='Test')
        self.assertTrue(check_password('testpassword123', user.password))

    def test_json(self):
        user = User.objects.get(first_name='Test')
        json = {
            'id': user.pk,
            'first_name': 'Test',
            'last_name': 'Testington',
            'email': 'test@gmail.com',
            'university': 'UVA',
            'has_meal_plan': True,
            'date_joined': date.today()
        }
        self.assertEqual(user.json(), json)

    def test_str(self):
        user = User.objects.get(first_name='Test')
        self.assertEqual('Test Testington', str(user))


class ListingTestCase(TestCase):
    def setUp(self):
        Listing.objects.create(
            user_id=1,
            title='Test',
            description='test post',
            listing_type='S',
            num_swipes=10
        )

    def test_json(self):
        listing = Listing.objects.get(description='test post')
        json = {
            'id': listing.pk,
            'title': 'Test',
            'description': 'test post',
            'user_id': 1,
            'listing_type': 'S',
            'num_swipes': 10,
            'last_modified': date.today()
        }
        self.assertEqual(listing.json(), json)

class AuthenticatorTestCase(TestCase):
    def setUp(self):
        Authenticator.objects.create(user_id=1)

    def test_length(self):
        auth = Authenticator.objects.get(user_id=1)
        self.assertEqual(len(auth.authenticator), 64)

    def test_auth_exists(self):
        auth = Authenticator.objects.get(user_id=1)
        self.assertTrue(auth.auth_exists(auth.authenticator))

    def test_is_expired(self):
        auth = Authenticator.objects.get(user_id=1)
        self.assertFalse(auth.is_expired())

    def test_json(self):
        auth = Authenticator.objects.get(user_id=1)
        json = {
            'user_id': 1,
            'authenticator': auth.authenticator,
            'date_created': date.today()
        }
        self.assertTrue(auth.json(), json)
