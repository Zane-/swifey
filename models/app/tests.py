from django.test import TestCase
from .models import User, Item
from tastypie.test import TestApiClient

import json

# set up api client
global client
client = TestApiClient()

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            first_name='Zane',
            last_name='Bilous',
            seller_status='True',
            email='zanebilous@gmail.com',
            university='University of Virginia'
        )
        User.objects.create(
            first_name='Sohan',
            last_name='Kabiraj',
            seller_status='True',
            email='sohan@gmail.com',
            university='University of Virginia'
        )
        User.objects.create(
            first_name='Bugi',
            last_name='Abdulkarim',
            seller_status='True',
            email='bugi@gmail.com',
            university='University of Virginia'
        )

    def testGet(self):
        response = client.get('/api/v1/user/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertEqual(d['first_name'], 'Zane')

    def testPost(self):
        response = client.post('/api/v1/user/', data={
            'first_name': 'Bugi',
            'last_name': 'Abdulkarim',
            'seller_status': False,
            'email': 'bugi@virginia.edu',
            'university': 'University of Virginia'
        })
        self.assertEqual(response.status_code, 201)

    def testPut(self):
        response = client.put('/api/v1/user/1/', data={
            'first_name': 'Zane',
            'last_name': 'Bilous',
            'seller_status': True,
            'email': 'zanebilous@virginia.edu',
            'university': 'University of Virginia'
        })
        self.assertEqual(response.status_code, 201)
        response = client.get('/api/v1/user/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertEqual(d['email'], 'zanebilous@virginia.edu')

    def testZDelete(self):
        response = client.delete('/api/v1/user/1/')
        self.assertEqual(response.status_code, 404)


class ItemTestCase(TestCase):
    def setUp(self):
        Item.objects.create(
            title="Looking for futon",
            description="Will trade 30 swipes for a used futon",
            created_by=2,
            num_swipes=30,
            label="S",
            for_swipes=False
        )
        Item.objects.create(
            title="Looking for futon",
            description="Will trade 30 swipes for a used futon",
            created_by=2,
            label="S",
            num_swipes=30,
            for_swipes=False
        )
        Item.objects.create(
            title="Looking for futon",
            description="Will trade 30 swipes for a used futon",
            created_by=2,
            num_swipes=30,
            label="S",
            for_swipes=False
        )

    def testGet(self):
        response = client.get('/api/v1/item/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertEqual(d['title'], 'Looking for futon')

    def testPost(self):
        response = client.post('/api/v1/item/', data={
            "title": "Looking for futon",
            "description": "Will trade 30 swipes for a used futon",
            "created_by": 2,
            "num_swipes": 30,
            "label": "S",
            "for_swipes": False })
        self.assertEqual(response.status_code, 201)

    def testPut(self):
        response = client.put('/api/v1/item/1/', data={
            "title": "Looking for futon",
            "description": "Will trade 30 swipes for a used futon",
            "created_by": 2,
            "num_swipes": 40,
            "label": "S",
            "for_swipes": False
        })
        self.assertEqual(response.status_code, 201)
        response = client.get('/api/v1/item/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertEqual(d['num_swipes'], 40)

    def testZDelete(self):
        response = client.delete('/api/v1/item/1/')
        self.assertEqual(response.status_code, 404)

    def testnumSwipes(self):
        response = client.put('/api/v1/item/1/', data={
            "title": "Looking for futon",
            "description": "Will trade 30 swipes for a used futon",
            "created_by": 2,
            "num_swipes": 40,
            "label": "S",
            "for_swipes": False
        })
        response = client.get('/api/v1/item/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertGreaterEqual(d['num_swipes'], 0)

    def testTradeIn(self):
        response = client.put('/api/v1/item/1/', data={
            "title": "Looking for futon",
            "description": "Will trade 30 swipes for a used futon",
            "created_by": 2,
            "num_swipes": 40,
            "label": "S",
            "for_swipes": False
        })
        response = client.get('/api/v1/item/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertNotEqual(d['created_by'], 1)

    def testLabelCheck(self):
        response = client.put('/api/v1/item/1/', data={
            "title": "Looking for futon",
            "description": "Will trade 30 swipes for a used futon",
            "created_by": 2,
            "num_swipes": 40,
            "label": "S",
            "for_swipes": False
        })
        response = client.get('/api/v1/item/1/')
        response = response.content.decode('ascii')
        d = json.loads(response)
        self.assertIn(d['label'], ('S', 'M'))
