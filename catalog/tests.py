# catalog/tests.py
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import SESSION_KEY
from django.views.defaults import page_not_found
from django.db import IntegrityError
from django.contrib.auth.models import User
from decimal import Decimal
import http


from catalog.models import Category, Product, ProductReview
from catalog.forms import ProductAddToCartForm


class NewUserTestCase(TestCase):
    """ tests an Anonymous user browsing the site pages """

    fixtures = ['catalog/fixtures/initial_data']

    def setUp(self):
        self.client = Client()
        # deprecated
        # logged_in = self.client.session.has_key(SESSION_KEY)
        # self.assertFalse(logged_in)
        self.assertFalse(SESSION_KEY in self.client.session)

    def test_view_homepage(self):
        home_url = reverse('catalog:catalog_home')
        response = self.client.get(home_url)
        # check that we get a response
        self.failUnless(response)
        # check that status code of response is success
        # (http.HTTPStatus.OK = 200)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_view_category(self):
        """ test category view loads """
        category = Category.active.all()[0]
        category_url = category.get_absolute_url()
        # get the template_name arg from URL entry
        url_entry = resolve(category_url)
        _template_name = url_entry[2]['template_name']
        # test loading of category page
        response = self.client.get(category_url)
        # test that we got a response
        self.failUnless(response)
        # test that the HTTP status code is "OK"
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # test that we used the category.html template in response
        self.assertTemplateUsed(response, _template_name)
        # test that category page contains category information
        self.assertContains(response, category.name)
        self.assertContains(response, category.description)

    def test_view_product(self):
        """
        test product view loads - similar to our category test
        """
        product = Product.active.all()[0]
        product_url = product.get_absolute_url()
        url_entry = resolve(product_url)
        _template_name = url_entry[2]['template_name']
        response = self.client.get(product_url)
        self.failUnless(response)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, _template_name)
        self.assertContains(response, product.name)
        self.assertContains(response, product.description)
        # check for cart form in product page response
        cart_form = response.context[0]['form']
        self.failUnless(cart_form)
        # check that the cart form is instance of correct form class
        self.failUnless(isinstance(cart_form, ProductAddToCartForm))
        # check for product reviews in product page response
        product_reviews = response.context[0].get('product_reviews', None)
        self.failIfEqual(product_reviews, None)


class ActiveProductManagerTestCase(TestCase):
    """
    tests that Product.active manager class returns only active products,
    and that inactive products return the 404 Not Found template
    """

    fixtures = ['catalog/fixtures/initial_data']

    def setUp(self):
        self.client = Client()

    def test_inactive_product_returns_404(self):
        """ test that inactive product returns a 404 error """
        inactive_product = Product.objects.filter(is_active=False)[0]
        inactive_product_url = inactive_product.get_absolute_url()
        # load the template file used to render the product page
        url_entry = resolve(inactive_product_url)
        _template_name = url_entry[2]['template_name']
        # load the name of the default django 404 template file
        django_404_template = page_not_found
        response = self.client.get(inactive_product_url)
        self.assertTemplateUsed(response, django_404_template)
        self.assertTemplateNotUsed(response, _template_name)


class ProductTestCase(TestCase):
    """
    tests the methods and custom properties on the catalog.Product model class
    """
    def setUp(self):
        self.product = Product.active.all()
        self.product.price = Decimal('199.99')
        self.product.save()
        self.client = Client()

    def test_sale_price(self):
        self.product.old_price = Decimal('220.00')
        self.product.save()
        self.failIfEqual(self.product.sale_price, None)
        self.assertEqual(self.product.sale_price, self.product.price)

    def test_no_sale_price(self):
        self.product.old_price = Decimal('0.00')
        self.product.save()
        self.failUnlessEqual(self.product.sale_price, None)

    def test_absolute_url(self):
        url = self.product.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_str(self):
        self.assertEqual(self.product.__str__(), self.product.name)


class ProductReviewTestCase(TestCase):
    """ tests the catalog.ProductReview model class """

    fixtures = ['initial_data']

    def test_orphaned_product_review(self):
        """
        attempt to save ProductReview instance with no product raises IntegrityError
        """
        pr = ProductReview()
        self.assertRaises(IntegrityError, pr.save)

    def test_product_review_defaults(self):
        """
        attempt to save ProductReview instance with fields empty resorts to class defaults
        """
        _user = User.objects.all()[0]
        _product = Product.active.all()[0]
        pr = ProductReview(user=_user, product=_product)
        pr.save()
        for field in pr._meta.fields:
            if field.has_default():
                self.assertEqual(pr.__dict__[field.name], field.default)
