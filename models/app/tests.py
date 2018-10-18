from django.test import TestCase
from .models import User, Item

# Create your tests here.

class UserTestCase(TestCase):

    # start up
    def setUp(self):
        pass

    # redirect client from home to details page
    def test_redirect_to_details(self):

    # tear down
    def tearDown(self):
        pass

class ItemTestCase(TestCase):

    # start up
    def setUp(self):
        pass

    # test if label is 's' or 'm'
    def test_label(self):
        self.assertIn(Item.label, ('s', 'm'))

    # test if number of swipes is greater than 1
    def test_num_swipes(self):
        self.assertGreaterEqual(Item.num_swipes, 0)

    # test if cost of swipe is greater than 1
    def test_cost(self):
        self.assertGreaterEqual(Item.cost, 0)

    # test that seller is not client and valid user
    def test_owner(self):
        self.assertNotEqual(Item.created_by.split(),
                            [User.first_name, User.last_name])
        # if separator is not a string then it failts
        with self.assertRaises(TypeError):
            Item.created_by.split(2)

    # tear down
    def tearDown(self):
        pass
