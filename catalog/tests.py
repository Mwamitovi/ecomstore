# catalog/tests.py
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import SESSION_KEY
import http

from catalog.models import Category


class NewUserTestCase(TestCase):

    fixtures = ['initial_data']

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




















