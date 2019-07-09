# catalog/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import SESSION_KEY
import http


class NewUserTestCase(TestCase):

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
