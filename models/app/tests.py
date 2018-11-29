import json
from datetime import date

from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase, Client
from .models import Authenticator, User, Listing

client = Client()

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
            'date_created': date.today(),
            'authenticator': auth.authenticator,
        }
        self.assertTrue(auth.json(), json)

class ApiTestCase(TestCase):
    """Tests the model api, which is identical for both User
    and Listing. Tests are run with the User model.
    """
    def setUp(self):
        User.objects.create(
            first_name='Test',
            last_name='Testington',
            email='test@gmail.com',
            password='testpassword123',
            has_meal_plan=True,
            university='UVA',
        )
        User.objects.create(
            first_name='Best',
            last_name='Bestington',
            email='Best@gmail.com',
            password='Bestpassword123',
            has_meal_plan=True,
            university='UVA',
        )
        User.objects.create(
            first_name='Jest',
            last_name='Jestington',
            email='jest@gmail.com',
            password='jestpassword123',
            has_meal_plan=True,
            university='UVA',
        )

    def test_get_model(self):
        user = User.objects.get(email='jest@gmail.com')
        pk = user.pk
        req = client.get('/api/v1/user/{}/'.format(pk))
        j = user.json()
        # convert datetime object to a string
        j['date_joined'] = str(j['date_joined'])
        self.assertEqual(req.json(), j)

    def test_post_model(self):
        data = {
            'first_name': 'Test1',
            'last_name': 'Test2',
            'email': 'testtest@gmail.com',
            'password': 'password123',
            'university': 'UVA'
        }
        bad_data = {
            'first_name': 'Test1',
            'last_name': 'Test2',
            'email': 'testtgmail.com',
            'password': 'password123',
            'university': 'UVA'
        }
        req = client.post('/api/v1/user/', data)
        self.assertEqual(req.status_code, 201)

        req = client.post('/api/v1/user/', data)
        self.assertEqual(req.status_code, 422)

    def test_update_model(self):
        data = {
            'first_name': 'Best',
            'last_name': 'Bestington',
            'email': 'newbest@gmail.com',
            'password': 'Bestpassword123',
            'university': 'UVA'
        }
        bad_data = {
            'first_name': 'Best',
            'last_name': 'Bestington',
            'email': 'newbestgmail.com',
            'password': 'Bestpassword123',
            'university': 'UVA'
        }
        user = User.objects.get(email='best@gmail.com')
        pk = user.pk
        req = client.post('/api/v1/user/{}/update/'.format(pk), data)
        self.assertEqual(req.status_code, 202)

        # verify email was changed
        user = User.objects.get(pk=pk)
        self.assertEqual(user.email, data['email'])

        req = client.post('/api/v1/user/2/', bad_data)
        self.assertEqual(req.status_code, 422)

        # verify email wasn't changed
        self.assertNotEqual(user.email, bad_data['email'])

    def test_delete_model(self):
        req = client.get('/api/v1/user/1/')
        self.assertNotEqual(req.status_code, 404)

        req = client.delete('/api/v1/user/1/')
        self.assertEqual(req.status_code, 202)

        # verify user was deleted
        req = client.get('/api/v1/user/1/')
        self.assertEqual(req.status_code, 404)

    def test_login(self):
        data = {'email': 'jest@gmail.com', 'password': 'jestpassword123'}
        bad_data = {'email': 'jest@gmail.com', 'password': 'bestpassword123'}

        req = client.post('/api/v1/login/', data)
        self.assertNotEqual(req.status_code, 401)

        req = client.post('/api/v1/login/', bad_data)
        self.assertEqual(req.status_code, 401)

    def test_validate_auth(self):
        user = User.objects.get(email='jest@gmail.com')
        pk = user.pk
        auth = {
            'authenticator': 'notavalidauth',
            'date_created': '2018-11-28',
            'user_id': pk
        }
        req = client.post('/api/v1/auth/', auth)
        self.assertEqual(req.status_code, 404)

        data = {'email': 'jest@gmail.com', 'password': 'jestpassword123'}

        req = client.post('/api/v1/login/', data)
        self.assertNotEqual(req.status_code, 401)
        auth = req.json()

        req = client.post('/api/v1/auth/', auth)
        self.assertEqual(req.status_code, 200)

    def test_validate_email(self):
        req = client.post('/api/v1/validate_email/', {'email': 'jest@gmail.com'})
        self.assertEqual(req.status_code, 409)

        req = client.post('/api/v1/validate_email/', {'email': 'notindb@gmail.com'})
        self.assertEqual(req.status_code, 200)
