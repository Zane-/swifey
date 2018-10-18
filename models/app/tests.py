from django.test import TestCase
from .models import User, Item

# Create your tests here.

class UserTestCase(TestCase):

    # start up
    def setUp(self):
        pass

    # redirect client from home to details page
    def redirect_to_details(self):

    # tear down
    def tearDown(self):
        pass

class ItemTestCase(TestCase):

    # start up
    def setUp(self):
        pass

    # test if label is 's' or 'm'
    def test_label(self):

    # test if number of swipes is greater than 1
    def test_num_swipes(self):

    # test if cost of swipe is greater than 1
    def test_cost(self):

    # test that seller is not client and valid user
    def test_owner(self):

    # tear down
    def tearDown(self):
        pass
