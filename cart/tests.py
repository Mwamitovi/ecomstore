# cart/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError
from django.middleware import csrf
from django.conf import settings
import http

from catalog.models import Product
from cart.models import CartItem
from cart import cart


class CartTestCase(TestCase):
    """ tests the functionality of the cart module """

    fixtures = ['catalog/fixtures/initial_data']

    def setUp(self):
        self.client = Client()
        self.product = Product.active.all()[0]

    def test_cart(self):
        home_url = reverse('catalog:catalog_home')
        self.client.get(home_url)
        # check that there is a cart_id set in session
        # after a page with cart box has been requested
        self.failUnless(self.client.session.get(cart.CART_ID_SESSION_KEY, ''))





































