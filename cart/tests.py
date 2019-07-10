# cart/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError
from http import HTTPStatus

from catalog.models import Product
from catalog.forms import ProductAddToCartForm
from cart.models import CartItem
from cart import cart


# noinspection PyPep8Naming
class CartTestCase(TestCase):
    """ tests the functionality of the cart module """

    fixtures = ['catalog/fixtures/initial_data']

    def setUp(self):
        self.client = Client()
        self.csrf_client = Client(enforce_csrf_checks=True)
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

    def test_add_product_empty_quantity(self):
        """
        POSTing a request with an empty quantity box will
        display 'required' form error message
        """
        product_url = self.product.get_absolute_url()
        postdata = {'product_slug': self.product.slug, 'quantity': ''}
        response = self.client.post(product_url, postdata)
        expected_error = str(
            ProductAddToCartForm.base_fields['quantity'].error_messages['required']
        )
        self.assertFormError(response, 'form', 'quantity', [expected_error])

    def test_add_product_zero_quantity(self):
        """
        POSTing a request with an 0 quantity will
        display 'min_value' form error message
        """
        product_url = self.product.get_absolute_url()
        postdata = {'product_slug': self.product.slug, 'quantity': 0}
        response = self.client.post(product_url, postdata)
        # need to concatenate the min_value onto error_text containing %s
        error_text = str(
            ProductAddToCartForm.base_fields['quantity'].error_messages['min_value']
        )
        _min_value = ProductAddToCartForm.base_fields['quantity'].min_value
        expected_error = error_text % _min_value
        self.assertFormError(response, 'form', 'quantity', [expected_error])

    def test_add_product_invalid_quantity(self):
        """
        POSTing a request with a non-integer quantity will
        display 'invalid' form error message
        """
        product_url = self.product.get_absolute_url()
        postdata = {'product_slug': self.product.slug, 'quantity': 'go'}
        response = self.client.post(product_url, postdata)
        expected_error = str(
            ProductAddToCartForm.base_fields['quantity'].error_messages['invalid']
        )
        self.assertFormError(response, 'form', 'quantity', [expected_error])

    def test_add_to_cart_fails_csrf(self):
        """
        adding product fails without including the
        CSRF token to POST request parameters
        """
        quantity = 2
        product_url = self.product.get_absolute_url()
        response = self.csrf_client.get(product_url)
        self.assertEqual(response.status_code, HTTPStatus.OK )
        # perform the post of adding to the cart
        postdata = {'product_slug': self.product.slug, 'quantity': quantity}
        response = self.csrf_client.post(product_url, postdata)
        # assert forbidden error due to missing CSRF input
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
