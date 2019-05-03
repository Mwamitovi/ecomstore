# checkout/checkout.py
from django.core.urlresolvers import reverse
import urllib
from cart import cart
from checkout.models import Order, OrderItem
from checkout.forms import CheckoutForm
from checkout import authnet
from ecomstore import settings


# noinspection PyUnusedLocal
def get_checkout_url(request):
    """ returns the URL from the checkout module for cart """

    # use this for our own-site checkout
    return reverse('checkout')
