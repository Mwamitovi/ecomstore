# cart/cart.py
from catalog.models import Product
from cart.models import CartItem
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from ecomstore import settings
import decimal
import random


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """ get the current user's cart id, sets new one if blank;
    Note: the syntax below matches the text, but an alternative,
    clearer way of checking for a cart ID would be the following:

    if not CART_ID_SESSION_KEY in request.session:
    """
    # if 'cart_id' in request.session:
    #     request.session['cart_id'] = _generate_cart_id()
    # return request.session['cart_id']
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """ function for generating random cart ID values """
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRQSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id


def get_cart_items(request):
    """ return all items from the current user's cart """
    return CartItem.objects.filter(cart_id=_cart_id(request))

