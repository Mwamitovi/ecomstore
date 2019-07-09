# catalog/tests.py
from django.test import TestCase, Client
from django.urls import reverse
import http


class NewUserTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_view_homepage(self):
        home_url = reverse('catalog:catalog_home')
        response = self.client.get(home_url)
        # check that we get a response
        self.failUnless(response)
        # check that status code of response is success
        # (http.HTTPStatus.OK = 200)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
