# cart/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError
from http import HTTPStatus

from catalog.models import Product
from cart.models import CartItem
from cart import cart


# noinspection PyPep8Naming
class CartTestCase(TestCase):
    """ tests the functionality of the cart module """

    fixtures = ['catalog/fixtures/initial_data']

    def setUp(self):
        self.client = Client()
        self.product = Product.active.all()[0]

    def test_cart(self):
        """
        A Cart ID gets set in the customer's session,
        after a page containing the cart box has been requested
        """
        home_url = reverse('catalog:catalog_home')
        self.client.get(home_url)
        # check that there is a cart_id set in session
        # after a page with cart box has been requested
        self.failUnless(self.client.session.get(cart.CART_ID_SESSION_KEY, ''))

    def get_cart_id(self):
        """ get test client's cart ID """
        return self.client.session.get(cart.CART_ID_SESSION_KEY)

    def get_cart_item_count(self):
        """
        get count of CartItem instances in test client shopping cart
        """
        _cart_id = self.get_cart_id()
        return CartItem.objects.filter(cart_id=_cart_id).count()

    def test_add_product(self):
        """
        POST request to a product page augments the CartItem instance count
        """
        QUANTITY = 2
        product_url = self.product.get_absolute_url()
        response = self.client.get(product_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # store count in cart_count variable
        cart_item_count = self.get_cart_item_count()
        # assert that the cart item count is zero
        self.failUnlessEqual(cart_item_count, 0)

        # perform the POST of adding to the cart
        # test client disables any CSRF checks by default
        postdata = {'product_slug': self.product.slug, 'quantity': QUANTITY}
        response = self.client.post(product_url, postdata)
        # confirm redirect to cart page - 302 then 200?
        cart_url = reverse('cart:show_cart')
        self.assertRedirects(
            response, cart_url,
            status_code=HTTPStatus.FOUND, target_status_code=HTTPStatus.OK
        )
        # check that cart item count is incremented by one
        self.assertEqual(self.get_cart_item_count(), cart_item_count + 1)

        _cart_id = self.get_cart_id()
        last_item = CartItem.objects.filter(cart_id=_cart_id).latest('date_added')
        # confirm if the latest cart item has a quantity of two
        self.failUnlessEqual(last_item.quantity, QUANTITY)
        # check if the latest cart item is the correct product
        self.failUnlessEqual(last_item.product, self.product)






































